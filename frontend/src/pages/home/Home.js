import Common from "../common/Common";
import React from "react";

export default class Home extends Common {
    constructor(props) {
        super(props);
        this.page_name = "Home";
    }

    body() {
        return (
            <div>
                Hello {this.state.username}, welcome to our {this.page_name} page
            </div>
        );
    }
    //
    // logged_out_message(){
    //     return this.body()
    // }
}