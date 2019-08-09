import React from 'react';
import './Common.scss';
import './../../../node_modules/font-awesome/css/font-awesome.min.css'
import Header from "../../components/header/Header";
import Footer from "../../components/footer/Footer";

import LoginForm from '../../components/LoginForm';
import SignupForm from '../../components/SignupForm';


export default class Common extends React.Component {

    constructor(props) {
        super(props);

        this.site_name = "Interview Calendar";
        this.year = new Date().getFullYear();
        this.page_name = "Common";
        this.backend_url = "http://0.0.0.0:8000";
        this.requires_login = true; // does this page require that the user is logged in?

        this.state = {
            displayed_form: '',
            logged_in: !!localStorage.getItem('token'),
            error_message: ''
        };
    }

    componentDidMount() {
        if (this.state.logged_in) {
            fetch(this.backend_url + '/accounts/current_user/', {
                headers: {
                    Authorization: `JWT ${localStorage.getItem('token')}`
                }
            })
                .then(res => res.json())
                .then(res => {
                    if (res.username) {
                        this.setState({username: res.username, user_type: res.user_type})
                    } else {

                        // invalidate the session
                        this.setState({username: '', user_type: '', logged_in: false});
                        localStorage.removeItem("token");
                    }
                });
        }
    }

    handle_login = (e, data) => {
        e.preventDefault();
        fetch(this.backend_url + '/token-auth/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(json => {
                if (json.token) {
                    localStorage.setItem('token', json.token);

                    this.setState({
                        logged_in: true,
                        displayed_form: '',
                        username: json.user.username,
                        user_type: json.user.user_type,
                        error_message: ""
                    });
                } else {
                    this.setState({error_message: "invalid password"});
                    console.log("invalid password", json)
                }
            });
    };

    handle_signup = (e, data) => {
        e.preventDefault();
        fetch(this.backend_url + '/accounts/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(json => {
                if (json.token) {
                    localStorage.setItem('token', json.token);
                    this.setState({
                        logged_in: true,
                        displayed_form: '',
                        username: json.username,
                        user_type: json.user_type,
                        error_message: ""
                    });
                } else {
                    this.setState({error_message: json.username});
                }
            });
    };

    handle_logout = () => {
        localStorage.removeItem('token');
        this.setState({logged_in: false, username: ''});
    };

    display_form = form => {
        this.setState({
            displayed_form: form,
            error_message: ""
        });
    };

    logged_out_message = () => {
        return (
            <div>
                Please Log In to view this page
            </div>
        )
    };

    body() {
        return (
            <div>
                Welcome to our {this.page_name} page
            </div>
        );
    }

    render() {
        let form;
        switch (this.state.displayed_form) {
            case 'login':
                form = <LoginForm handle_login={this.handle_login}  error_message={this.state.error_message}/>;
                break;
            case 'signup':
                form = <SignupForm handle_signup={this.handle_signup} error_message={this.state.error_message}/>;
                break;
            default:
                form = null;
        }

        return (
            <div className="app container-fluid">
                <Header
                    site_name={this.site_name}
                    page_name={this.page_name}
                    logged_in={this.state.logged_in}
                    logged_in_user={this.state.username}
                    logged_in_user_type={this.state.user_type}
                    display_form={this.display_form}
                    handle_logout={this.handle_logout}
                />
                <div className="body">
                    {
                        this.requires_login ? (this.state.logged_in ? this.body() : this.logged_out_message()): this.body()
                    }
                    {form}
                </div>
                <Footer site_name={this.site_name} year={this.year}/>
            </div>
        );
    }
}


