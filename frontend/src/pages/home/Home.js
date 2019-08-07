import Common from "../common/Common";
import React from "react";
import Calendar from 'react-calendar'
// import './Home.scss';

export default class Home extends Common {
    constructor(props) {
        super(props);
        this.page_name = "Home";

        this.date = new Date()

    }

    onChange = date => this.setState({ date });
    onClickDay = (value) => alert('Clicked day: '+ value);
    tileClassName=({ date, view }) => view === 'month' && date.getDay() === 3 ? 'wednesday' : null;

    body() {
        return (
            <div>
                Hello {this.state.username}, welcome to our {this.page_name} page
                <Calendar
                    onChange={this.onChange}
                    value={this.date}
                    minDate={new Date()}
                    calendarType="US"
                    selectRange={true}
                    // tileClassName={this.tileClassName}
                    // onClickDay={this.onClickDay}
                />
            </div>
        );
    }
    //
    // logged_out_message(){
    //     return this.body()
    // }
}