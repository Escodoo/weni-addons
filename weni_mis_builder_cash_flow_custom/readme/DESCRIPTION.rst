This module extends the functionality of the ``mis.cash_flow.forecast_line`` model in Odoo to include additional information about related records and associated analytic accounts, as well as actions to directly access the related records and their parent records.

Features
--------

1. **Additional fields**:

   - ``res_id``: stores the ID of the related record.
   - ``res_model_id``: stores a reference to the related document model.
   - ``res_model``: stores the name of the related document model.
   - ``parent_res_id``: stores the ID of the related parent record.
   - ``parent_res_model_id``: stores a reference to the related parent document model.
   - ``parent_res_model``: stores the name of the related parent document model.
   - ``analytic_account_id``: stores a reference to the associated analytic account.

2. **Method ``action_open_document_related``**:

   - Opens the view of the related record in Odoo.
   - Returns ``False`` if the ``res_model`` and ``res_id`` fields are empty.

3. **Method ``action_open_parent_document_related``**:

   - Opens the view of the related parent record in Odoo.
   - Returns ``False`` if the ``parent_res_model`` and ``parent_res_id`` fields are empty.
