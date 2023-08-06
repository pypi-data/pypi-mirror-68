# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.notebook import NodeCells
import nbformat as nbf

class TTVSetsSplitterNodeCells(NodeCells):
    def _body_cells(self):
        value_cell = nbf.v4.new_code_cell(f"# TODO: Implement later")

        return [value_cell]
