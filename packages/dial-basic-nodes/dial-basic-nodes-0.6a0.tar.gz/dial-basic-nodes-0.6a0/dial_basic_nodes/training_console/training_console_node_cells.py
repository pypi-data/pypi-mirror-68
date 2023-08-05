# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import nbformat as nbf

from dial_core.notebook import NodeCells


class TrainingConsoleNodeCells(NodeCells):
    def _body_cells(self):
        model_var = self._node.inputs["Model"].word_id()
        hyperparameters_var = self._node.inputs["Hyperparameters"].word_id()
        train_dataset_var = self._node.inputs["TTV Sets"].word_id()
        trained_model_var = self._node.outputs["Trained Model"].word_id()

        compile_source = (
            f"{trained_model_var} = keras.models.Model(\n"
            f"    Input({train_dataset_var}.input_shape),\n"
            f"    {model_var}\n"
            f")\n"
            f"{trained_model_var}.compile(\n"
            f"    optimizer={hyperparameters_var}['optimizer'],\n"
            f"    loss={hyperparameters_var}['loss_function'],\n"
            f"    metrics=['accuracy']\n"
            f")"
        )

        summary_source = f"{trained_model_var}.summary()"

        fit_source = (
            f"{trained_model_var}.fit(\n"
            f"{train_dataset_var},\n"
            f"epochs={hyperparameters_var}['epochs'],\n"
            f")"
        )

        return [
            nbf.v4.new_code_cell(compile_source),
            nbf.v4.new_code_cell(summary_source),
            nbf.v4.new_code_cell(fit_source),
        ]
