// Imports: Dependencies
import {
  legacy_createStore as createStore,
  applyMiddleware,
  compose,
} from 'redux';
import createSagaMiddleware from 'redux-saga';

// Imports: Redux Root Reducer
import rootReducer from '../reducers';

// Imports: Redux Root Saga
import rootSaga from '../sagas/rootSaga';

// Middleware: Redux Saga
const sagaMiddleware = createSagaMiddleware();

const middleware = [sagaMiddleware];

// const composeEnhancers = window._REDUX_DEVTOOLS_EXTENSION_COMPOSE_;
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

// Redux: Store
const store = createStore(
  rootReducer,
  composeEnhancers(applyMiddleware(...middleware)),
);

// Middleware: Redux Saga
sagaMiddleware.run(rootSaga);

// Exports
export default store;
