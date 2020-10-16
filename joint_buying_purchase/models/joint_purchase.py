from odoo import fields, models


class JointBuyingPurchaseOrder(models.Model):
    _name = "joint.buying.purchase.order"
    _description = "Joint buying purchase order"
    _rec_name = "supplier_id"

    tour_id = fields.Many2one("joint.buying.tour", string="Tour")

    customer_id = fields.Many2one(
        "res.partner",
        string="Joint customer",
        required=True,
        domain=[("is_joint_buying_customer", "=", True)]
    )

    supplier_id = fields.Many2one(
        "res.partner",
        string="Joint buying supplier",
        required=True,
        domain=[("is_joint_buying_supplier", "=", True)]
    )

    line_ids = fields.One2many(
        "joint.buying.purchase.order.line",
        inverse_name="order_id",
        sting="Lines for each customer"
    )

    pivot_activity = fields.Char(compute="_get_pivot_activity", store=True)

    def _get_pivot_activity(self):
        if self.supplier_id.activity_id:
            return self.supplier_id.activity_id.name
        return self.supplier_id.name


class JointBuyingPurchaseOrderLine(models.Model):
    _name = "joint.buying.purchase.order.line"
    _description = "Joint buying purchase order line"

    order_id = fields.Many2one("joint.buying.purchase.order", string="Order")

    product_id = fields.Many2one(
        "product.product", string="Product", domain=[("is_joint_buying", "=", True)]
    )
    quantity = fields.Float()
