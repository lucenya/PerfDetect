from datetime import datetime

ucm_tenant_public_id = "9b0d7ef3-3fc5-4821-8bbe-a32bcb0e155e"
ucm_service_id = "20352"
operator_alias = "ucmicmr"
transfer_render_type = "Plaintext"

kusto_ppe_ingest_connection = "https://ingest-bingadsppe.kusto.windows.net"
kusto_production_ingest_connection = "https://ingest-bingads.kusto.windows.net"

# icm config
debug_mode_enabled = True

# template
str_datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
transfer_comment_template = "Auto transfer to {team_name}"
max_fetch_retry_time = 3

# model
use_default_model = False


