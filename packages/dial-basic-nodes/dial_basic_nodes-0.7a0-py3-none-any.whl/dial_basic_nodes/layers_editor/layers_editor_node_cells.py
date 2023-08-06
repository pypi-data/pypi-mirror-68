# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import nbformat as nbf
from dial_core.notebook import NodeCells


class LayersEditorNodeCells(NodeCells):
    def _body_cells(self):
        model = self._node.get_model()

        sequence_code = (
            f"{self._node.outputs['Model'].word_id()} = keras.models.Sequential([\n"
        )
        for layer in model.layers:
            sequence_code += (
                f"keras.layers.{type(layer).__name__}."
                f"from_config({str(layer.get_config())}),\n"
            )

        sequence_code += "])"

        return [nbf.v4.new_code_cell(sequence_code)]
