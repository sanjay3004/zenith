// library imports
import React from 'react';
import { SafeAreaView } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';

// screens
import Home from '../Screens/Home';
import Splash from '../Screens/Splash';
import Login from '../Screens/Login';

// constants
import * as CONSTANTS from '../constants';

// object destructurings
const { HOME, LOGIN } = CONSTANTS.screenTitles;

const Stack = createStackNavigator();

const MainStack = () => {
  // const { loading, token } = props;
  // if (loading) {
  //   return (
  //     <SafeAreaView style={{ flex: 1 }}>
  //       <Splash />
  //     </SafeAreaView>
  //   );
  // }
  return (
      <SafeAreaView style={{ flex: 1 }}>
        <Stack.Navigator>
          {true ? (
          //   Login screen
            <Stack.Screen
              name={LOGIN}
              component={Login}
              options={{
                headerShown: false,
              }}
            />
          ) : (
          //   Home screen
            <Stack.Screen
              name={HOME}
              component={Home}
              options={{
                headerShown: false,
              }}
            />
          )}
        </Stack.Navigator>
      </SafeAreaView>
  );
};

export default MainStack;
