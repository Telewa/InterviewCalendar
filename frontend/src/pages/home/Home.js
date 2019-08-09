import Common from "../common/Common";
import React from "react";
// import './Home.scss';

export default class Home extends Common {
    constructor(props) {
        super(props);
        this.page_name = "Home";
        this.date = new Date();
        this.requires_login = false;
    }

    body() {
        return (
            <div>
                Welcome to our {this.page_name} page
            </div>
        );
    }
}