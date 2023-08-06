import error_explainer
from thonny import get_workbench
from thonny.assistance import ProgramAnalyzer, add_program_analyzer


class ErrorExplainer(ProgramAnalyzer):
    def is_enabled(self):
        return get_workbench().get_option("assistance.use_error_explainer")

    def start_analysis(self, main_file_path, imported_file_paths):
        found_errors = error_explainer.check_runner.run_checks(main_file_path)
        warnings = []
        for error in found_errors:
            warnings.append({
                    "filename": main_file_path,
                    "msg": "(error-explainer) " + error,
            })
        self.completion_handler(self, warnings)


def load_plugin():
    for k, v in error_explainer.messages._messages.items():
        error_explainer.messages.overwrite_message(k, v.replace("\n", " "))

    get_workbench().set_default("assistance.use_error_explainer", True)
    get_workbench().add_command(command_id="error-explainer",
                                menu_name="tools",
                                command_label="error-explainer enabled?",
                                flag_name="assistance.use_error_explainer")
    add_program_analyzer(ErrorExplainer)
