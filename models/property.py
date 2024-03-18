from odoo import fields, models, api
from datetime import date, timedelta


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Property'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string="Available From",
                                    default=date.today() + timedelta(days=90),
                                    copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    best_price = fields.Float(string="Best Price", compute="_compute_best_price", readonly=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="GardenArea")
    garden_orientation = fields.Selection([("north", "North"),
                                           ("south", "South"),
                                           ("east", "East"),
                                           ("west", "West")],
                                          string="Garden Orientation",
                                          default="north")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([("new", "New"),
                              ("offer received", "Offer Received"),
                              ("offer accepted", "Offer Accepted"),
                              ("sold", "Sold"),
                              ("canceled", "Canceled")],
                             required=True,
                             copy=False,
                             default="new",
                             string="Status")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    offer_ids = fields.One2many("estate.property.offer",
                                "property_id",
                                string="Offers")
    seller_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    total_area = fields.Integer(string="Total Area",
                                compute=_compute_total_area,
                                readonly=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            offers = rec.offer_ids.mapped('price')
            rec.best_price = max(offers) if offers else 0.0
