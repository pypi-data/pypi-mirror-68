from aoa.model_utility.base_model import BaseModel
from aoa.model_utility.model_utility import ModelUtility
import json
import os
import subprocess
import sys
import logging


class EvaluateModel(BaseModel):

    def __init__(self, model_utility: ModelUtility):
        super().__init__(model_utility)
        self.logger = logging.getLogger(__name__)

    def evaluate_model_local(self, model_id: str = None, base_path: str = None, data_conf: dict = None):
        base_path = self.model_utility.model_catalog_path if base_path is None else os.path.join(base_path, '')
        model_path = base_path + 'model_definitions/'

        if not os.path.exists(model_path):
            raise ValueError("model directory {0} does not exist".format(model_path))

        if model_id is None:
            if "id" in self.model_utility.model:
                model_id = self.model_utility.model["id"]
            else:
                BaseModel.get_model_id(model_path)

        model_artefacts_path = ".artefacts/{}".format(model_id)

        try:
            os.symlink(model_artefacts_path, "./models", target_is_directory=True)

            model_dir = model_path + model_id

            cli_model_kargs = {
                "model_id": model_id,
                "model_version": "cli",
                "model_table": "AOA_MODELS_cli"
            }

            with open(model_dir + "/model.json", 'r') as f:
                model_definition = json.load(f)

            with open(model_dir + "/config.json", 'r') as f:
                model_conf = json.load(f)

            self.logger.info("Loading and executing model code")

            engine = self._BaseModel__get_engine(model_definition)
            if engine == "python" or engine == "pyspark":
                if engine == "pyspark":
                    self._BaseModel__configure_pyspark(model_definition, model_artefacts_path)

                sys.path.append(model_dir)
                import model_modules
                model_modules.scoring.evaluate(data_conf, model_conf, **cli_model_kargs)

            elif engine == "sql":
                self.__evaluate_sql(model_dir, data_conf, model_conf, **cli_model_kargs)

            elif engine == "R":
                cmd = self.model_utility.dir_path + "/run_model.R {} {} {} {}".format(model_id, "evaluate", dataset_path, base_path)
                subprocess.check_call(cmd, shell=True)

            else:
                raise Exception("Unsupported language: {}".format(model_definition["language"]))

            self.logger.info("Artefacts can be found in: {}".format(model_artefacts_path))
            self.logger.info("Evaluation metrics can be found in: {}/evaluation.json".format(model_artefacts_path))
            self.__cleanup()
        except:
            self.__cleanup()
            raise

    def __cleanup(self):
        os.remove("./models")

    def __evaluate_sql(self, model_dir, data_conf, model_conf, **kwargs):
        from teradataml import create_context
        from teradataml.dataframe.dataframe import DataFrame
        from teradataml.context.context import get_connection

        self.logger.info("Starting evaluation...")

        create_context(host=data_conf["hostname"],
                       username=os.environ["TD_USERNAME"],
                       password=os.environ["TD_PASSWORD"],
                       logmech=os.getenv("TD_LOGMECH", "TDNEGO"))

        sql_file = model_dir + "/model_modules/scoring.sql"
        jinja_ctx = {
            "data_conf": data_conf,
            "model_conf": model_conf,
            "model_table": kwargs.get("model_table"),
            "model_version": kwargs.get("model_version"),
            "model_id": kwargs.get("model_id")
        }

        self._BaseModel__execute_sql_script(get_connection(), sql_file, jinja_ctx)

        self.logger.info("Finished evaluation")

        stats = DataFrame(data_conf["metrics_table"]).to_pandas()
        metrics = dict(zip(stats.key, stats.value))

        with open("models/evaluation.json", "w+") as f:
            json.dump(metrics, f)

        self.logger.info("Saved metrics")
