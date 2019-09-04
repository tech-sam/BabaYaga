import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import './App.scss';

import Header from './layout/Header';
import Dashboard from './dashboard/Dashboard';

class App extends Component {

    render(){
      return (
        <div className="App">
          <Header/>
          <Dashboard />
        </div>
      ) 
    }
}
ReactDOM.render(<App />, document.getElementById('app'));