import React from "react";
import {BrowserRouter as Router, Route} from "react-router-dom";
import Home from "./pages/home/Home";
import About from "./pages/about/About";
import Settings from "./pages/settings/Settings";
import Account from "./pages/account/Account";

export default function CalendarRoutes() {
    return (
        <Router>
            <Route exact path="/" component={Home}/>
            <Route path="/about" component={About}/>
            <Route path="/settings" component={Settings}/>
            <Route path="/account" component={Account}/>
        </Router>
    );
}

