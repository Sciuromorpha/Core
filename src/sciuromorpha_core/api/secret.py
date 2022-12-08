from typing import Any, Union

from nameko.rpc import rpc

from sqlalchemy import select

from sciuromorpha_core import model, static as S
from sciuromorpha_core.db.session import SessionFactory


class Secret:
    name = "secret"

    @rpc
    def create_or_update(self) -> dict:
        pass

    @rpc
    def get(self, service_meta: dict) -> Union[dict, None]:
        with SessionFactory.begin() as session:
            stmt = select(model.Secret).where(
                model.Secret.service == service_meta["name"]
                and model.Secret.key == service_meta["secret_key"]
            )

            data = session.execute(stmt).first()

            if data is None:
                return None

        return data
