"""Helper functions for getting data

Notes
-----
All functions must have a `sess` argument so that multiple functions can be
called while retaining object data from queried objects.
"""

from sqlalchemy import select, func

from .tables import TEROSData, PowerData

import datetime

def get_power_data(sess, cell_id, resample="hour"):
    """Gets the power data for a given cell. Can be directly passed to
    bokeh.ColumnDataSource.

    Parmaters
    ---------
    sess : sqlalchemy.orm.Session
        Session to use
    cell_id : int
        Valid Cell.id

    Returns
    -------
    dict
        Dictionary of lists with keys named after columns of the table
        {
            'timestamp': [],
            'v': [],
            'i': [],
            'p': []
        }
    """

    data = {
        'timestamp': [],
        'v': [],
        'i': [],
        'p': [],
    }

    current_time = datetime.datetime.today()
    one_day_ago = current_time - datetime.timedelta(days = 45)

    resampled = (
        select(
            func.date_trunc(resample, PowerData.ts).label("ts"),
            func.avg(PowerData.voltage).label("voltage"),
            func.avg(PowerData.current).label("current")
        )
        .where(PowerData.cell_id == cell_id and PowerData.ts >= one_day_ago)
        .group_by(func.date_trunc(resample, PowerData.ts))
        .subquery()
    )

    adj_units = (
        select(
            resampled.c.ts.label("ts"),
            (resampled.c.voltage * 10e-9).label("voltage"),
            (resampled.c.current * 10e-6).label("current")
        )
        .subquery()
    )

    stmt = (
        select(
            adj_units.c.ts.label("ts"),
            adj_units.c.voltage.label("voltage"),
            adj_units.c.current.label("current"),
            (adj_units.c.voltage * adj_units.c.current).label("power")
        )
        .order_by(adj_units.c.ts)
    )

    for row in sess.execute(stmt):
        data["timestamp"].append(row.ts)
        data["v"].append(row.voltage)
        data["i"].append(row.current)
        data["p"].append(row.power)

    return data

def get_teros_data(sess, cell_id, resample='hour'):
    """Gets the TEROS-12 sensor data for a given cell. Returned dictionary can
    be passed directly to bokeh.ColumnDataSource.

    Parmaters
    ---------
    s : sqlalchemy.orm.Session
        Session to use
    cell_id : int
        Valid Cell.id
    resample : str
        Resample time frame. Defaults to hour.  Valid options are
        [microseconds, milliseconds, second, minute, hour, day, week, month,
        quarter, year, decade, century, millennium].

    Returns
    -------
    dict
        Dictionary of lists with keys named after columns of the table
        {
            'timestamp': [],
            'vwc': [],
            'temp': [],
            'ec': []
        }
    """

    data = {
        'timestamp': [],
        'vwc': [],
        'temp': [],
        'ec': []
    }

    stmt = (
        select(
            func.date_trunc(resample, TEROSData.ts).label("ts"),
            func.avg(TEROSData.vwc).label("vwc"),
            func.avg(TEROSData.temp).label("temp"),
            func.avg(TEROSData.ec).label("ec")
        )
        .where(TEROSData.cell_id == cell_id)
        .group_by(func.date_trunc(resample, TEROSData.ts))
        .order_by(func.date_trunc(resample, TEROSData.ts))
    )

    for row in sess.execute(stmt):
        data['timestamp'].append(row.ts)
        data['vwc'].append(row.vwc)
        data['temp'].append(row.temp)
        data['ec'].append(row.ec)

    return data
