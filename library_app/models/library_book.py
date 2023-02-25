from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class Book(models.Model):
    _name = "library.book"
    _description = "Book"
    _order = "name, date_published desc"
    name = fields.Char("Title", required=True)
    isbn = fields.Char("ISBN")
    book_type = fields.Selection(
        [("paper", "Paperback"),
         ("hard", "Hardcover"),
         ("electronic", "Electronic"),
         ("other", "Other")],
        "Type"
    )
    notes = fields.Text("Internal Notes")
    descr = fields.Html("Description")
    copies = fields.Integer(default=1)
    avg_rating = fields.Float("Average Rating", (3, 2))
    price = fields.Monetary("Price", "currency_id")
    currency_id = fields.Many2one("res.currency")
    date_published = fields.Date()
    last_borrow_date = fields.Datetime(
        "Last Borrowed On",
        default=lambda self: fields.Datetime.now())
    active = fields.Boolean("Active?", default=True)
    image = fields.Binary("Cover")

    publisher_id = fields.Many2one("res.partner",
                                   string="Publisher")
    author_ids = fields.Many2many(comodel_name="res.partner",
                                  string="Authors")
    
    @api.depends("publisher_id.country_id")
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id
        
    def _inverse_publisher_country(self):
        for book in self:
            book.publisher_id.country_id = book.publisher_country_id
    
    def _search_publisher_country(self, operator, value):
        return [("publisher_id.country_id", operator, value)]

    
    publisher_country_id = fields.Many2one(
        "res.country",
        string="Publisher Country",
        compute="_compute_publisher_country",
        inverse="_inverse_publisher_country",
        search="_search_publisher_country"
    )

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError(
                    "Please provide an ISBN for %s " % book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is invalid" % book.isbn)
        return True

    @api.constrains("isbn")
    def _constraint_isbn_valid(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError(
                    "%s is an invalid ISBN" % book.isbn
                )

    _sql_constraints = [
        ("library_book_name_date_uq",
         "UNIQUE (name, date_published)",
         "Title and publication date must be unique."),
        ("library_book_check_date",
         "CHECK (date_published <= current_date)",
         "Publication date must not be in the future."),
    ]
