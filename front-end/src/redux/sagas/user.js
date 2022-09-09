import {all, put, takeLatest, call} from 'redux-saga/effects';
import { loginApiService } from '../../api';
import {fetchUserSuccess, fetchUserError, loginSuccess, loginError} from '../actions/user';
import {USER_FETCH_LOADING, LOGIN_LOADING} from '../types/user';

function* loginSaga(action){
  try {
    const loginResponse = yield call(loginApiService, action.payload);
    yield put(loginSuccess(loginResponse));
  } catch (error) {
    yield put(loginError());
  }
}

function* fetchUserSaga(action) {
  try {
    yield put(fetchUserSuccess());
  } catch (error) {
    yield put(fetchUserError());
  }
}

function* workerSaga() {
  yield takeLatest(USER_FETCH_LOADING, fetchUserSaga);
  yield takeLatest(LOGIN_LOADING, loginSaga);
}

function* userSagas() {
  yield all([call(workerSaga)]);
}
export {userSagas};
