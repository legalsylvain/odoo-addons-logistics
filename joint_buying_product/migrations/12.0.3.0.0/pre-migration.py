# Copyright (C) 2023-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(
        env.cr, "joint_buying_purchase_order_line", "pivot_company_id"
    ):
        openupgrade.logged_query(
            env.cr,
            """
            ALTER TABLE joint_buying_purchase_order_line
            ADD COLUMN pivot_company_id int;
            """,
        )
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE joint_buying_purchase_order_line jbpol
            SET pivot_company_id = jbpo.pivot_company_id
            FROM joint_buying_purchase_order jbpo
            WHERE jbpol.order_id = jbpo.id;
            """,
        )
