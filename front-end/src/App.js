// Imports: Dependencies
import 'react-native-gesture-handler';
import React from 'react';
import {Provider} from 'react-redux';

import MainNavigation from './navigation';

// Imports: Redux Store
import store from './redux/store';

// React Native App
const App = () => {
  return (
    // Redux: Global Store
    <Provider store={store}>
      <MainNavigation />
    </Provider>
  );
};
export default App;