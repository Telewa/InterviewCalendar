import React from 'react';
import './Header.scss';
import {Link} from "react-router-dom";
import Nav from "../Nav";


class Header extends React.Component {
    constructor(props){
        super(props);
        this.user_types = {
            1: "admin",
            2: "interviewer",
            3: "candidate",
        };
    }

    render() {
        return (
            <div>
                <div className="header">
                    <h1>{this.props.site_name}</h1>
                    <h4>{this.props.page_name}</h4>
                    <h6>{this.user_types[this.props.logged_in_user_type]}</h6>
                </div>
                <nav className="navbar navbar-expand-lg navbar-light bg-light">
                    <button className="navbar-toggler" type="button" data-toggle="collapse"
                            data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false"
                            aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"/>
                    </button>
                    <div className="collapse navbar-collapse" id="menu">
                        <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
                            <li className="nav-item">
                                <Link to="/" className="nav-link fa fa-home"> Home</Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/about" className="nav-link fa fa-info"> About US</Link>
                            </li>

                            <li className="nav-item">
                                <Link to="/settings" className="nav-link fa fa-gears"> Settings</Link>
                            </li>
                        </ul>
                        <Nav
                            logged_in={this.props.logged_in}
                            display_form={this.props.display_form}
                            handle_logout={this.props.handle_logout}
                            logged_in_user={this.props.logged_in_user}
                        />
                    </div>
                </nav>
            </div>
        );
    }
}

export default Header