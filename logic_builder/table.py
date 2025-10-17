from functools import partial
from typing import Any, Callable, TypeVar, Generic, TypedDict, cast


type ColumnName = str
type GetFunction = Callable[[ColumnName], Any]
type Formula = Callable[[GetFunction], Any]
T = TypeVar('T')
type RowFilter = Callable[[GetFunction], bool]
type ColumnFilter = Callable[[ColumnName, list[Any]], bool]


class Wrapper(Generic[T]):
    """A simple wrapper class to hold a value of type T."""
    _object: T

    def __init__(self, value: 'T | Wrapper[T]'):
        if isinstance(value, Wrapper):
            self._object = cast(T, value._object)
        else:
            assert not isinstance(value, Wrapper)
            self._object = value

    @property
    def object(self) -> T:
        return self._object

    @object.setter
    def object(self, new: T):
        self._object = new

    def __setattr__(self, name: str, value: Any) -> None:
        if name == '_object':
            super().__setattr__(name, value)
        else:
            setattr(self._object, name, value)

    def __getattribute__(self, name: str) -> Any:
        return getattr(self._object, name)


class Column(TypedDict):
    type: type
    formula: Formula | None
    values: list[Wrapper[Any]]


class Table:
    def __init__(self):
        self.columns: dict[ColumnName, Column] = {}
        self.rows: list[dict[ColumnName, Wrapper[Any]]] = []

        # Filters
        # Row filters take a function that allows them getting the value of a column in the current row
        self.row_filters: list[RowFilter] = []
        # Column filters take the column name and all its values
        self.column_filters: list[ColumnFilter] = []

    def add_column(
        self,
        name: ColumnName,
        data_type: type = str,
        formula: Formula | None = None
    ):
        """Add a column with optional formula"""
        self.columns[name] = Column({
            'type': data_type,
            'formula': formula,
            'values': []
        })

    def add_row(self, **kwargs: Any):
        """Add a row with column values"""
        row = {}
        self.rows.append(row)
        for col_name in self.columns:
            formula = self.columns[col_name]['formula']
            if col_name in kwargs:
                row[col_name] = Wrapper(kwargs[col_name])
            elif formula is not None:
                row[col_name] = Wrapper(formula(partial(self.get_value, row_index=len(self.rows))))
            else:
                row[col_name] = None
        print(row['1'][0])

    def sum_column(self, column_name: ColumnName) -> float:
        """Calculate sum of values in a column"""
        if column_name not in self.columns:
            raise ValueError(f"Column {column_name} not found")
        total = 0.0
        for row in self.rows:
            value = row.get(column_name)
            if value is not None:
                unwrapped = value.object
                if isinstance(unwrapped, (int, float)):
                    total += unwrapped
        return total

    def filter(
        self,
        condition: list[RowFilter | ColumnFilter] | RowFilter | ColumnFilter
    ) -> list[dict[ColumnName, Wrapper[Any]]]:
        """Filter rows based on condition function"""
        raise NotImplementedError("Filter method is not implemented yet")

    def get_value(self, row_index: int, column_name: ColumnName) -> Any | None:
        """Get value at specific row and column"""
        if 0 <= row_index < len(self.rows):
            val = self.rows[row_index].get(column_name)
            if val is not None:
                return val.object
        return None

    def set_value(self, row_index: int, column_name: ColumnName, value: Any):
        """Set value at specific row and column"""
        if 0 <= row_index < len(self.rows) and column_name in self.columns:
            self.rows[row_index][column_name].object = value
