{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Import Dependencies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Restarting with stat\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\wargo\\Anaconda3\\lib\\site-packages\\IPython\\core\\interactiveshell.py:3334: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "\n",
    "# ---------------------- STEP 2: Climate APP\n",
    "\n",
    "from flask import Flask, json, jsonify\n",
    "import datetime as dt\n",
    "\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "from sqlalchemy import inspect\n",
    "\n",
    "engine = create_engine(\"sqlite:///./Resources/hawaii.sqlite\", connect_args={'check_same_thread': False})\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)\n",
    "\n",
    "# Save references to each table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "session = Session(engine)\n",
    "\n",
    "app = Flask(__name__) # the name of the file & the object (double usage)\n",
    "\n",
    "# List all routes that are available.\n",
    "@app.route(\"/\")\n",
    "def home():\n",
    "    print(\"In & Out of Home section.\")\n",
    "    return (\n",
    "        f\"Welcome to the Climate API!<br/>\"\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/2016-01-01/<br/>\"\n",
    "        f\"/api/v1.0/2016-01-01/2016-12-31/\"\n",
    "    )\n",
    "\n",
    "# Return the JSON representation of your dictionary\n",
    "@app.route('/api/v1.0/precipitation/')\n",
    "def precipitation():\n",
    "    print(\"In Precipitation section.\")\n",
    "    \n",
    "    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date\n",
    "    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)\n",
    "\n",
    "    rain_results = session.query(Measurement.date, Measurement.prcp).\\\n",
    "    filter(Measurement.date >= last_year).\\\n",
    "    order_by(Measurement.date).all()\n",
    "\n",
    "    p_dict = dict(rain_results)\n",
    "    print(f\"Results for Precipitation - {p_dict}\")\n",
    "    print(\"Out of Precipitation section.\")\n",
    "    return jsonify(p_dict) \n",
    "\n",
    "# Return a JSON-list of stations from the dataset.\n",
    "@app.route('/api/v1.0/stations/')\n",
    "def stations():\n",
    "    print(\"In station section.\")\n",
    "    \n",
    "    station_list = session.query(Station.station)\\\n",
    "    .order_by(Station.station).all() \n",
    "    print()\n",
    "    print(\"Station List:\")   \n",
    "    for row in station_list:\n",
    "        print (row[0])\n",
    "    print(\"Out of Station section.\")\n",
    "    return jsonify(station_list)\n",
    "\n",
    "# Return a JSON-list of Temperature Observations from the dataset.\n",
    "@app.route('/api/v1.0/tobs/')\n",
    "def tobs():\n",
    "    print(\"In TOBS section.\")\n",
    "    \n",
    "    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date\n",
    "    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)\n",
    "\n",
    "    temp_obs = session.query(Measurement.date, Measurement.tobs)\\\n",
    "        .filter(Measurement.date >= last_year)\\\n",
    "        .order_by(Measurement.date).all()\n",
    "    print()\n",
    "    print(\"Temperature Results for All Stations\")\n",
    "    print(temp_obs)\n",
    "    print(\"Out of TOBS section.\")\n",
    "    return jsonify(temp_obs)\n",
    "\n",
    "# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date\n",
    "@app.route('/api/v1.0/<start_date>/')\n",
    "def calc_temps_start(start_date):\n",
    "    print(\"In start date section.\")\n",
    "    print(start_date)\n",
    "    \n",
    "    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]\n",
    "    result_temp = session.query(*select).\\\n",
    "        filter(Measurement.date >= start_date).all()\n",
    "    print()\n",
    "    print(f\"Calculated temp for start date {start_date}\")\n",
    "    print(result_temp)\n",
    "    print(\"Out of start date section.\")\n",
    "    return jsonify(result_temp)\n",
    "\n",
    "# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.\n",
    "@app.route('/api/v1.0/<start_date>/<end_date>/')\n",
    "def calc_temps_start_end(start_date, end_date):\n",
    "    print(\"In start & end date section.\")\n",
    "    \n",
    "    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]\n",
    "    result_temp = session.query(*select).\\\n",
    "        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()\n",
    "    print()\n",
    "    print(f\"Calculated temp for start date {start_date} & end date {end_date}\")\n",
    "    print(result_temp)\n",
    "    print(\"Out of start & end date section.\")\n",
    "    return jsonify(result_temp)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
