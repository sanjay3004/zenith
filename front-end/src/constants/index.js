import Config from "react-native-config";

const screenTitles = {
  SPLASH: 'Splash',
  HOME: 'Home',
  LOGIN: 'Login',
};

const RoutingConstants = {
  login: '/api/authaccount/login',
  register: '/api/authaccount/registration',
  users: '/api/users?page=1'
};

const BASE_URL = "http://restapi.adequateshop.com";

export {screenTitles, RoutingConstants, BASE_URL};
