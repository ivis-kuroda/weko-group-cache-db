#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Signal definitions for weko-group-cache-db."""

from blinker import signal

# Define a custom signal for updating count
update_count_signal = signal("update_count")

# Define a custom signal for updating result
update_result_signal = signal("update_result")
