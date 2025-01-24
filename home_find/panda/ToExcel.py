import pandas as pd

from django.forms.models import model_to_dict


class ToExcel:
    @staticmethod
    def export_excel(home_infos, dry_run=False, file_path=None):

        if not isinstance(home_infos, dict):
            home_infos = [model_to_dict(home_info) for home_info in home_infos]

        if dry_run:
            for num, home_info in enumerate(home_infos):
                home_info["id"] = num
                home_info.pop("price_cal", None)
                home_info.pop("created_at", None)
                home_info.pop("updated_at", None)
                home_info.pop("deleted_at", None)

        data = {key: [item[key] for item in home_infos] for key in home_infos[0].keys()}

        df = pd.DataFrame(data)

        df["website"] = '=HYPERLINK("' + df["website"] + '", "' + df["website"] + '")'

        df.to_excel(file_path or "output.xlsx", index=False)

        return True
