# Create Needed classes for later
import json
from .tools import Formula


class List:
    def __init__(self, list_, name):
        self.content = list_
        self.name = name


class Cell:
    def __init__(self, x, y, content=None):
        self.y = y
        self.x = x
        self.content = content

    def object(self):
        return self

    def get_content(self, target_cell_value=None):
        if self.content.__class__.__name__ == 'Formula':
            return self.content.get_value(target_cell_value)
        return self.content

    def change(self, new_content):
        self.content = new_content

    def json(self):
        if self.content.__class__.__name__ == 'Formula':
            return {"type": "Formula", "content": self.content.json()}
        else:
            return {"type": "Normal", "content": self.content}


# Create custom errors.
class Error(Exception):
    pass


class SpreadsheetError(Error):
    pass


# create the spreadsheet class
class Spreadsheet:
    def __init__(self, x_len, y_len):
        self.x_axis_list = []
        self.y_axis_list = []
        self.y_len = y_len
        self.x_len = x_len
        self.output = []
        for y in range(y_len):
            a_list = []
            for x in range(x_len):
                a_list.append(Cell(x, y, None))
            self.y_axis_list.append(List(a_list, y))

        for x in range(x_len):
            a_list = []
            for content in self.y_axis_list:
                a_list.append(content.content[x])
            self.x_axis_list.append(List(a_list, x))

    def create_from_json(self, path_to_file, **kwargs):
        with open(path_to_file, "r") as j:
            load_file = json.load(j)

        if "sheet" not in load_file:
            return SpreadsheetError("Not a valid sheet JSON")

        sheet = load_file.get("sheet")
        new_sheet = Spreadsheet(len(sheet.keys()), len(sheet.get("x0").keys()))

        for column in list(sheet.keys()):
            for row in sheet.get(column):
                cell = sheet.get(column).get(row)
                if cell.get("type") == "Formula":
                    content = cell.get("content").get("formula")
                    new_sheet.change_cell(int(column[1:2]), int(row[1:2]), Formula(kwargs.get(content.get("name")), content.get("target")))
                else:
                    content = cell.get("content")
                    new_sheet.change_cell(int(column[1:2]), int(row[1:2]), content)

        return new_sheet

    def get_cell(self, x, y):
        try:
            if self.x_axis_list[x].content[y] == self.y_axis_list[y].content[x]:
                cell = self.y_axis_list[y].content[x]
                if cell.content.__class__.__name__ == "Formula":
                    return cell.get_content(self.get_cell(*cell.content.get_target()))
                else:
                    return cell.get_content()
        except IndexError:
            raise SpreadsheetError(f'Requested index is outside of spreadsheet boundaries. {x, y}')

    def get_cell_obj(self, x, y):
        try:
            if self.x_axis_list[x].content[y] == self.y_axis_list[y].content[x]:
                cell = self.y_axis_list[y].content[x]
                return cell.object()
        except IndexError:
            raise SpreadsheetError(f'Requested index is outside of spreadsheet boundaries. {x, y}')

    def change_cell(self, x, y, new_content):
        try:
            if self.x_axis_list[x].content[y] == self.y_axis_list[y].content[x]:
                self.x_axis_list[x].content[y].object().change(new_content)
                self.y_axis_list[y].content[x].object().change(new_content)
            self.update_formulas()
        except IndexError:
            raise SpreadsheetError('Requested index is outside of spreadsheet boundaries.')

    def get_format_self_tuple(self, spaces=2):
        formatted_tuple = []
        for a in self.get_self_tuple():
            for b in a:
                if len(str(b)) > spaces:
                    spaces = len(str(b))

        for a in self.get_self_tuple():
            a_list = []
            for b in a:
                a_list.append(' ' * (spaces - len(str(b))) + str(b))
            formatted_tuple.append(tuple(a_list))

        formatted_tuple = tuple(formatted_tuple)
        return formatted_tuple

    def get_self_tuple(self):
        return tuple(
            tuple(
                self.get_cell(x, y) for x in range(self.x_len)
            ) for y in range(self.y_len)
        )

    def reset_output(self):
        self.output = []

    def pretty_print(self):
        self.pretty_output()
        for i in self.output:
            print(i)
        self.reset_output()
        print()

    def pretty_output(self, formatting=2):
        self._output_grid(sub_tuples=self.get_format_self_tuple(formatting))

    def _output_grid(self, sub_tuple=None, sub_tuples=None):
        for i in range(self.y_len):
            x_axis = '|%s' * self.x_len
            if sub_tuple is None and sub_tuples is None:
                self.output.append(x_axis)
            elif sub_tuple is None:
                try:
                    self.output.append(x_axis % sub_tuples[i])
                except TypeError:
                    raise SpreadsheetError('Invalid tuple length for sub_tuple.')
            else:
                try:
                    self.output.append(x_axis % sub_tuple)
                except TypeError:
                    raise SpreadsheetError('Invalid tuple length for sub_tuple.')
            self.output.append('-' * len(str(x_axis % sub_tuples[i])))

    def update_formulas(self):
        pass

    def json(self):
        cells_dict = {}
        for x in range(self.x_len):
            y_dict = {}
            for y in range(self.y_len):
                y_dict["y%s" % y] = self.get_cell_obj(x,y).json()

            cells_dict["x%s" % x] = y_dict

        return {"sheet": cells_dict}
