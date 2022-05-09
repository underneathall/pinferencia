import itertools
import os
import re
from typing import Dict, List, Optional

import strictyaml
from pydantic import BaseModel


class BaseMixin:
    assets_path: Optional[str] = "docs/"

    def validate_path(self):
        raise NotImplementedError("Not Implemented")


class MarkDownMixin:
    @property
    def md_files(self) -> List[str]:
        """
        Get files ending in md from docs
        """
        matches = []
        for root, _, filenames in os.walk(self.assets_path):
            matches.extend(
                os.path.join(root, filename)
                for filename in filenames
                if filename.endswith((".md"))
            )
        return matches


class MkdocsParse(BaseMixin, BaseModel):
    path: Optional[str] = "mkdocs.yml"
    default_language: str = "en"
    languages_excluded: Optional[list] = ["re"]

    def read(self) -> list:
        """
        Read content from path file
        """
        assert os.path.exists(self.path), f"Path {self.path} not exists"
        with open(self.path, "r") as f:
            content = f.read()
        return content.split("nav:")

    @property
    def languages(self) -> list:
        """
        Languages supported by mkdocs
        """
        languages = list(
            strictyaml.load(
                self.read()[0].split("languages:")[1].split("nav_translations")[0]
            ).data.keys()
        )
        for language in self.languages_excluded:
            if language in languages:
                languages.remove(language)
        return languages

    @property
    def nav(self) -> list:
        """
        mkdocs navigation info
        """
        return strictyaml.load(self.read()[1]).data

    @property
    def nav_title(self):
        """
        mkdocs navigation title
        """
        nav_title_list = []
        self.list_to_list(self.nav, nav_title_list)
        return nav_title_list

    @property
    def translations(self):
        """
        mkdocs translation info
        """
        return strictyaml.load(
            self.read()[0]
            .split("languages:")[1]
            .split("nav_translations:")[1]
            .split("markdown_extensions")[0]
        ).data

    def list_to_list(self, data: list, data_list: list) -> None:
        # sourcery skip: raise-specific-error
        """
        convert list to list
        """
        for i in data:
            for key, value in i.items():
                if key not in data_list:
                    data_list.append(key)
                if isinstance(value, list):
                    self.list_to_list(value, data_list)
                elif isinstance(value, str):
                    continue
                else:
                    raise Exception("Invalid markdown config.")

    def list_to_dict(self, data: list, data_dict: dict) -> None:
        # sourcery skip: raise-specific-error
        """
        convert list to dict
        """
        for i in data:
            for key, value in i.items():
                if isinstance(value, list):
                    self.list_to_dict(value, data_dict)
                elif isinstance(value, str):
                    data_dict[value] = key
                else:
                    raise Exception("Invalid markdown config.")

    @property
    def nav_dict(self) -> dict:
        """
        convert navigation yaml info to dict
        """
        nav_dict = {}
        self.list_to_dict(self.nav, nav_dict)
        return nav_dict

    def validate_path(self) -> tuple:
        """
        compare the paths of nav
        """
        # nav_translations_mismatch = {}
        nav_mismatch = {}
        for key, value in self.nav_dict.items():
            for language in self.languages:
                key_replace = (
                    key.replace(".md", f".{language}.md")
                    if language != self.default_language
                    else key
                )
                if not os.path.exists(
                    os.path.join(self.assets_path.rstrip("/"), key_replace)
                ):
                    nav_mismatch[f"{language}-{value}"] = key_replace
        return nav_mismatch

    def validate_title(self):
        return {
            f"{language}-{title}": language
            for title, language in itertools.product(self.nav_title, self.languages)
            if language != self.default_language
            and title not in self.translations[language]
        }


class AssetsParse(BaseMixin, MarkDownMixin, BaseModel):
    assets: Optional[dict] = {
        "images": "assets/images",
        "download": "assets/download",
    }

    def validate_assets_path(
        self,
        row: int,
        match: list,
        module: str,
        result: Dict = "",
    ) -> dict:
        """
        Args:
            row: The number of rows where the assets is located
            match: Regular  matching result
            module: assets type
            result: validate result
                if not match:
                    return Dict[str, str]
                else:
                    return {}
        """
        for index, value in enumerate(match):
            if not os.path.exists(os.path.join(self.assets_path, value.lstrip("/"))):
                item = (
                    {f"{row}-{module}{index}": value}
                    if index > 0
                    else {f"{row}-{module}": value}
                )
                result.update(item)
        return result

    def validate_path(self) -> dict:
        """
        Compare the paths of assets (images, downloads)

        if not match:
            return Dict[str, List[Dict[str, str]]]
        else:
            return {}
        """
        assets_mismatch_info = {}
        for file in self.md_files:
            try:
                with open(file, "r") as f:
                    for row, line in enumerate(f):
                        mismatch_info = {}
                        for module, assets in self.assets.items():
                            if assets in line:
                                pattern = re.compile(r"\((.+?)\)")
                                mismatch_info = self.validate_assets_path(
                                    row,
                                    pattern.findall(line),
                                    module,
                                    mismatch_info,
                                )
                        if not len(mismatch_info):
                            continue
                        info = assets_mismatch_info.get(file, [])
                        info.append(mismatch_info)
                        assets_mismatch_info[file] = info
            except Exception as exc:
                raise exc
        return assets_mismatch_info
