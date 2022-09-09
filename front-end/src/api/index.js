// library imports
import axios from 'axios';

// constants
import {RoutingConstants, BASE_URL} from '../constants';

/**
 * @function login
 * @param {Object} payload
 * @returns {JSON}
 */
export const loginApiService = async (payload = {}) => {
  const {login} = RoutingConstants;
  const loginUrl = `${BASE_URL}${login}`;
  try {
    const response = await axios.post(loginUrl, payload, {timeout: 10000});
    return response.data;
  } catch (error) {
    return error;
  }
};

/**
 * @function register
 * @param {Object} payload
 * @returns {JSON}
 */
export const registerApiService = async (payload = {}) => {
  const {register} = RoutingConstants;
  const registerUrl = `${BASE_URL}${register}`;
  try {
    const response = await axios.post(registerUrl, payload);
    return response.data;
  } catch (error) {
    return error;
  }
};
