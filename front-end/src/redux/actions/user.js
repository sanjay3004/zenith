import {
  LOGIN_LOADING,
  LOGIN_SUCCESS,
  LOGIN_ERROR,
  USER_FETCH_LOADING,
  USER_FETCH_SUCCESS,
  USER_FETCH_ERROR,
} from '../types/user';

const loginRequest = (payload = {}) => {
  return {type: LOGIN_LOADING, payload};
};

const loginSuccess = (response = {}) => {
  return {type: LOGIN_SUCCESS, response};
};

const loginError = (response = {}) => {
  return {type: LOGIN_ERROR, error};
};

const fetchUser = (payload = {}) => ({
  type: USER_FETCH_LOADING,
  payload: payload,
});

const fetchUserSuccess = (response = {}) => ({
  type: USER_FETCH_SUCCESS,
  response: response,
});

const fetchUserError = (error = {}) => ({type: USER_FETCH_ERROR, error: error});

export {
  loginRequest,
  loginSuccess,
  loginError,
  fetchUser,
  fetchUserSuccess,
  fetchUserError,
};
