#!/bin/env python3
"""A simple cost calculator for your various backup schemes."""

import random

FULL_INTERVAL = 30
FULL_INITIAL_SIZE = 500
PARTIAL_INTERVAL = 1
PARTIAL_SIZE = 0.1
PARTIAL_SIZE_VAR = (-5, 5)
RETENTION = 90

TIME_RANGES = [30, 60, 90, 180, 360]
PRICE_MINIMUM = 4.99
PRICE_PER_UNIT = PRICE_MINIMUM/1024
MINIMUM_STORAGE_TIME = 90
BACKUP_TYPE = {'full': 0, 'partial': 1}


class bpayload():
    """A type for our backups."""

    def __init__(self, tstamp, btype, bsize, parent=None):
        """Init bpayload()."""
        self.tstamp = tstamp
        self.btype = btype
        self.bsize = bsize
        if btype == BACKUP_TYPE['full']:
            self.parent = None
        elif btype == BACKUP_TYPE['partial'] and isinstance(parent, bpayload):
            self.parent = parent
        else:
            raise TypeError()

        self.deleted = False


def calculate_cost(date, backups, price_mnimum, price_per_unit):
    """Take a list o backup objects present and return a summary of cost."""
    cummulative_size = 0

    for backup in backups:
        cummulative_size += backup.bsize

    if cummulative_size == 0:
        cost = 0
    elif cummulative_size <= 1024:
        cost = price_mnimum
    else:
        cost = cummulative_size*price_per_unit

    return (int(date/30), cummulative_size, cost)


def wasabicalc(parameters):
    """Run the program."""
    random.seed()

    FULL_INTERVAL = parameters['full_interval']
    FULL_INITIAL_SIZE = parameters['full_initial_size']
    PARTIAL_INTERVAL = parameters['partial_interval']
    PARTIAL_SIZE = parameters['partial_size']
    PARTIAL_SIZE_VAR = parameters['partial_size_var']
    RETENTION = parameters['retention']

    TIME_RANGES = parameters['time_ranges']
    PRICE_MINIMUM = parameters['price_minimum']
    PRICE_PER_UNIT = PRICE_MINIMUM/1024
    MINIMUM_STORAGE_TIME = parameters['minimum_storage_time']
    BACKUP_TYPE = {'full': 0, 'partial': 1}

    elapsed_time = 0
    latest_parent = None
    source_size = FULL_INITIAL_SIZE
    cost_raport = []

    backups = []

    if latest_parent is None:
        backups.append(bpayload((elapsed_time), 0, source_size))

    for day in range(TIME_RANGES[-1]):
        elapsed_time += 1
        # Daily - cleanup of deleted elements over 90 days old
        for backup in backups:
            # print("{0}, {1}".format(backup.tstamp, elapsed_time))
            if backup.tstamp + MINIMUM_STORAGE_TIME <= elapsed_time and backup.deleted is True:
                backups.remove(backup)

        # On FULL_INTERVAL - full backup
        if day % FULL_INTERVAL == 0:
            backups.append(bpayload((elapsed_time), 0, source_size))

        # On PARTIAL_INTERVAL - partial backup
        elif day % PARTIAL_INTERVAL == 0:
            size_delta = random.uniform(PARTIAL_SIZE_VAR[0], PARTIAL_SIZE_VAR[1]) + PARTIAL_SIZE
            source_size += size_delta
            backups.append(bpayload((elapsed_time), 1, size_delta, backups[-1]))

        # Monthly - cost calculation
        if day % 30 == 0:
            cost_raport.append(calculate_cost(day, backups, PRICE_MINIMUM, PRICE_PER_UNIT))

        # Daily - retention check
        for backup in backups:
            if backup.btype == BACKUP_TYPE['full']:
                if backup.tstamp + RETENTION <= elapsed_time:
                    backup.deleted = True
            if backup.btype == BACKUP_TYPE['partial']:
                if backup.parent.deleted is True:
                    backup.deleted = True

    return cost_raport


def main():
    """Run the program."""
    random.seed()

    elapsed_time = 0
    latest_parent = None
    source_size = FULL_INITIAL_SIZE
    cost_raport = []

    backups = []

    if latest_parent is None:
        backups.append(bpayload((elapsed_time), 0, source_size))

    for day in range(TIME_RANGES[-1]):
        elapsed_time += 1
        # Daily - cleanup of deleted elements over 90 days old
        for backup in backups:
            # print("{0}, {1}".format(backup.tstamp, elapsed_time))
            if backup.tstamp + MINIMUM_STORAGE_TIME <= elapsed_time and backup.deleted is True:
                backups.remove(backup)

        # On FULL_INTERVAL - full backup
        if day % FULL_INTERVAL == 0:
            backups.append(bpayload((elapsed_time), 0, source_size))

        # On PARTIAL_INTERVAL - partial backup
        elif day % PARTIAL_INTERVAL == 0:
            size_delta = random.uniform(PARTIAL_SIZE_VAR[0], PARTIAL_SIZE_VAR[1]) + PARTIAL_SIZE
            source_size += size_delta
            backups.append(bpayload((elapsed_time), 1, size_delta, backups[-1]))

        # Monthly - cost calculation
        if day % 30 == 0:
            cost_raport.append(calculate_cost(day, backups, PRICE_MINIMUM, PRICE_PER_UNIT))

        # Daily - retention check
        for backup in backups:
            if backup.btype == BACKUP_TYPE['full']:
                if backup.tstamp + RETENTION <= elapsed_time:
                    backup.deleted = True
            if backup.btype == BACKUP_TYPE['partial']:
                if backup.parent.deleted is True:
                    backup.deleted = True

    for month in cost_raport:
        print("{0}:\t Size:\t {1} GB\t Cost:\t ${2}".format(month[0]+1, round(month[1], 2), round(month[2], 3)))

    print(cost_raport)


if __name__ == '__main__':
    main()
