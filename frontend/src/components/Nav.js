import React from 'react';
import PropTypes from 'prop-types';
import {Link} from "react-router-dom";

export default function Nav(props) {
    const logged_out_nav = (
        <ul className="navbar-nav mt-2 mt-lg-0">
            <li  className="nav-item" >
                <Link to={null} onClick={() => props.display_form('login')} className="nav-link fa fa-lock"> login</Link>
            </li>
            <li  className="nav-item">
                <Link to={null} onClick={() => props.display_form('signup')} className="nav-link fa fa-user"> Signup</Link>
            </li>
        </ul>
    );

    const logged_in_nav = (
        <ul className="navbar-nav mt-2 mt-lg-0">
            <li  className="nav-item" >
                <Link to={null} onClick={props.handle_logout} className="nav-link fa fa-unlock"> Sign out ({props.logged_in_user})</Link>
            </li>
        </ul>
    );
    return props.logged_in ? logged_in_nav : logged_out_nav;
}


Nav.propTypes = {
    logged_in: PropTypes.bool.isRequired,
    display_form: PropTypes.func.isRequired,
    handle_logout: PropTypes.func.isRequired
};