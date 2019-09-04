import React, {Component} from 'react'
import './Dashboard.scss'
import SourceServer from '../source-server/SourceServer';
import DestinationServer from '../destination-server/DestinationServer';


class Dashboard extends Component {
    render() {
        return (
            <section className='container'>
                <div className="source">
                    <SourceServer/>
                </div>
                <div className="destination">
                    <DestinationServer/>
                </div>
            </section>
        )
    }
}

export default Dashboard