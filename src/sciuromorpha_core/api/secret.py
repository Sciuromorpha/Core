from typing import Any, Union

from nameko.rpc import rpc

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from sciuromorpha_core import model, static as S
from sciuromorpha_core.db.session import SessionFactory
from sciuromorpha_core.exceptions import ArgumentMissingError


class Secret:
    name = "secret"

    @rpc
    def put(self, service_meta: dict) -> dict:
        # Params check.
        # TODO: Use schema or Pydantic to check.
        if (
            service_meta.get("name", None) is None
            or service_meta.get("secret_key", None) is None
        ):
            raise ArgumentMissingError("service_meta need both name&secret_key exists.")

        with SessionFactory.begin() as session:
            data = service_meta.get("secret_data", None)
            stmt = insert(model.Secret).values(
                service=service_meta["name"],
                key=service_meta["secret_key"],
                data=data,
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=["service", "key"], set_=dict(data=stmt.excluded.data)
            )

            print(stmt)
            result = session.execute(stmt).fetchall()
            print(result)

        return {}

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
