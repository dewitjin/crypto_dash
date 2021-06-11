import get_data
import config
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = config.APP_FLASK_SECRET_KEY


@app.route("/")
def index():
    title = "Crypto Dash"
    return render_template("index.html", title=title)


@app.route("/chart")
def chart(low_time_frame_data=[], high_time_frame_data=[], selected_symbols="", selected_date_start="",
          selected_date_end=""):
    title = "Charts"
    symbols = get_data.get_symbols()
    low_time_frame_data = low_time_frame_data
    high_time_frame_data = high_time_frame_data
    selected_symbols = selected_symbols
    selected_date_start = selected_date_start
    selected_date_end = selected_date_end
    return render_template("chart_form.html", title=title, symbols=symbols,
                           low_time_frame_data=low_time_frame_data, high_time_frame_data=high_time_frame_data,
                           selected_symbols=selected_symbols, selected_date_start=selected_date_start,
                           selected_date_end=selected_date_end)


@app.route("/plot", methods=['POST'])
def plot():
    try:

        low_time_frame_data = []
        high_time_frame_data = []

        # data returns a list with objects then is turn to json with js on frontend
        if len(request.form["date_start"]) != 0 and len(request.form["date_end"]) != 0:
            low_time_frame_data = get_data.get_low_time_frame_data(request.form["symbols"], request.form["date_start"],
                                                                   request.form["date_end"])
            high_time_frame_data = get_data.get_high_time_frame_data(request.form["symbols"],
                                                                     request.form["date_start"],
                                                                     request.form["date_end"])
            flash("Form data submitted", "Success")
        else:
            flash("Please enter data in all fields", "Success")
    except Exception as e:
        # If message attribute is not found, then e is an object that is not json serializable
        # so convert to string to read.
        flash(e.message if hasattr(e, 'message') else str(e), "Error")

    return chart(low_time_frame_data, high_time_frame_data, request.form["symbols"], request.form["date_start"],
                 request.form["date_end"])


@app.route("/csv")
def csv_report():
    title = "CSV Reports"
    return render_template("csv.html", title=title)


@app.route("/balance")
def balance():
    title = "My balances"
    my_balances = get_data.get_balance()
    return render_template("balance.html", title=title, my_balances=my_balances)


@app.route("/download_last_prices_data/")
def download_last_prices_data():
    return get_data.get_last_prices()


@app.route("/download_interval_data")
def download_1day_interval_report_for_btcusdt_data():
    return get_data.get_1day_interval_report_for_btcusdt()
