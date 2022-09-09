import {combineReducers} from 'redux';
import userReducer from './user';

const AppReducer = combineReducers({user: userReducer});

export default AppReducer;