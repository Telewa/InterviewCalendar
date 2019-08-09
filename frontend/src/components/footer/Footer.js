import React from 'react';
import './Footer.scss'
import PropTypes from 'prop-types';

class Footer extends React.Component {
    render() {
        return (
            <div className="footer">
                &copy; {this.props.site_name} {this.props.year}
            </div>
        );
    }
}

export default Footer


Footer.propTypes = {
    site_name: PropTypes.string.isRequired,
    year: PropTypes.number.isRequired,
};
