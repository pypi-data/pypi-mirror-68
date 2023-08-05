import inspect
from io import BytesIO
from zipfile import ZipFile, ZipInfo

import stringcase
from typing import Type, Dict

import typing
from django.db import models
from djmoney.models.fields import MoneyField

from avishan.configure import get_avishan_config
from avishan.models import AvishanModel


class ChayiWriter:
    def __init__(self):
        self.files = {}
        self.tab_size = 0
        for model in AvishanModel.get_models():
            if model._meta.abstract or model.export_ignore:
                continue
            self.files[model.class_name() + ".java"] = self.model_file_creator(model)

        self.model_file_predefined_models(self.files)
        # todo datetime, date, time, image file

        self.compress_files(self.files)

    def model_file_creator(self, model: Type[AvishanModel]) -> str:
        data = self.model_file_head()

        data += f'\n\npublic class {model.class_name()} extends Chayi' + ' {\n\n'
        self.tab_size = 4

        data += self.model_file_write_fields(model)
        data += self.model_file_write_constructor(model)
        data += self.model_file_write_names(model)
        data += self.model_file_write_getter_setters(model)

        data += '    @Override\n' \
                '    public boolean equals(Object o) {\n' \
                '        if (this == o) return true;\n' \
                '        if (o == null || getClass() != o.getClass()) return false;\n' \
                f'        {model.class_name()} temp = ({model.class_name()}) o;\n' \
                '        return this.id == temp.id;\n' \
                '    }\n'

        data += "}"

        return data

    def compress_files(self, files: Dict[str, str]):
        archive = BytesIO()
        with ZipFile(archive, 'w') as zip_archive:
            for key, value in files.items():
                file = ZipInfo(key)
                zip_archive.writestr(file, value)

        with open('chayi_models.zip', 'wb') as f:
            f.write(archive.getbuffer())

        archive.close()

    @staticmethod
    def model_file_head() -> str:
        return f'package {get_avishan_config().CHAYI_PROJECT_PACKAGE}.models;\n\nimport ir.coleo.chayi.Chayi;\n' + \
               ChayiWriter.model_file_head_imports()

    def tab_before(self) -> str:
        return self.tab_size * " "

    @staticmethod
    def model_file_head_imports() -> str:
        return get_avishan_config().CHAYI_MODEL_FILE_IMPORTS

    def model_file_write_fields(self, model: Type[AvishanModel]) -> str:
        data = ''
        for field in model.get_fields():
            if field.name == 'id':
                continue
            data += self.model_file_write_field(model, field)

        return data

    def model_file_write_constructor(self, model: Type[AvishanModel]) -> str:
        # todo default values
        create_method = getattr(model, 'create')
        data = "\n" + self.tab_before() + \
               f'public {model.class_name()}('
        for name, param in dict(inspect.signature(create_method).parameters.items()).items():
            if param.name == 'kwargs':
                raise ValueError(f'Create function for model {model.class_name()} not found')
            data += f'{self.model_file_write_param_type(param.annotation)} {name}, '
        if data.endswith(', '):
            data = data[:-2]
        data += ") {\n"

        for name in dict(inspect.signature(create_method).parameters.items()):
            data += self.tab_before() + f"    this.{name} = {name};\n"
        data += self.tab_before() + "}\n"
        return data

    def model_file_write_getter_setters(self, model: Type[AvishanModel]) -> str:
        data = ''
        for field in model.get_fields():
            if field.name == 'id':
                continue
            data += \
                f'    public {self.model_file_write_field_type(model, field)} ' \
                f'{stringcase.camelcase("get_" + field.name)}' \
                + "() {" + \
                f'\n        return {field.name};' \
                '\n    }' \
                '\n' \
                f'\n    public void ' \
                f'{stringcase.camelcase("set_" + field.name)}' \
                + f"({self.model_file_write_field_type(model, field)} {field.name}) " + "{" + \
                f'\n        this.{field.name} = {field.name};' \
                '\n    }' \
                '\n' \
                '\n'
        return data

    @staticmethod
    def model_file_write_names(model: Type[AvishanModel]) -> str:
        return f'\n    public static String getPluralName() ' \
               '{' \
               f'\n        return "{model.class_plural_snake_case_name()}";' \
               '\n    }' \
               '\n' \
               '\n    public static String getSingleName() {' \
               f'\n        return "{model.class_snake_case_name()}";' \
               '\n    }\n\n'

    def model_file_write_field(self, model: [AvishanModel], field: models.Field) -> str:
        data = self.tab_before() + '@Expose'
        if model.is_field_readonly(field):
            data += '(serialize = false)'
        data += '\n' + self.tab_before() + "private " + self.model_file_write_field_type(model,
                                                                                         field) + " " + field.name + ";\n"

        return data

    def model_file_write_field_type(self, model: Type[AvishanModel], field: models.Field) -> str:

        if isinstance(field, (models.AutoField, models.IntegerField, MoneyField)):
            return 'int'
        if isinstance(field, models.ForeignKey):
            return field.related_model.class_name()
        if isinstance(field, models.DateTimeField):
            return 'DateTime'
        if isinstance(field, (models.CharField, models.TextField)):
            return 'String'
        if isinstance(field, models.BooleanField):
            return 'boolean'
        if isinstance(field, models.FloatField):
            return 'double'
        if isinstance(field, models.ImageField):
            return 'Image'
        if isinstance(field, models.FileField):
            return 'File'
        raise NotImplementedError()

    def model_file_write_param_type(self, annotation: inspect.Parameter) -> str:
        if isinstance(annotation, models.base.ModelBase):
            return annotation.class_name()
        if annotation is bool:
            return 'boolean'
        if annotation is str:
            return 'String'
        if annotation is int:
            return 'int'
        if annotation is float:
            return 'double'
        if isinstance(annotation, str):
            return annotation
        if isinstance(annotation, typing._Union) and len(annotation.__args__) == 2:
            return self.model_file_write_param_type(annotation.__args__[0])
        raise NotImplementedError()

    def model_file_predefined_models(self, files: dict):
        files['DateTime.java'] = """package ir.zimaapp.citizen.models;

import ir.coleo.chayi.Chayi;

import com.google.gson.annotations.Expose;

public class DateTime {

    String day_name;
    String month_name;
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
    int microsecond;

}"""
        files['Date.java'] = """package ir.zimaapp.citizen.models;

import ir.coleo.chayi.Chayi;

import com.google.gson.annotations.Expose;

public class Date {

    String day_name;
    String month_name;
    int year;
    int month;
    int day;
                                  
}"""
        files['Time.java'] = """package ir.zimaapp.citizen.models;

import ir.coleo.chayi.Chayi;

import com.google.gson.annotations.Expose;

public class Time {

    int hour;
    int minute;
    int second;
    int microsecond;

}"""
        files['Image.java'] = """package ir.zimaapp.citizen.models;

import ir.coleo.chayi.Chayi;

import com.google.gson.annotations.Expose;

public class Image {

    String url;
    int id;

}"""
        files['File.java'] = """package ir.zimaapp.citizen.models;

import ir.coleo.chayi.Chayi;

import com.google.gson.annotations.Expose;

public class File {

    String url;
    int id;

}"""
