import {all, call} from 'redux-saga/effects';
import {userSagas} from './user';
function* rootSaga() {
  yield all([call(userSagas)]);
}
export default rootSaga;
