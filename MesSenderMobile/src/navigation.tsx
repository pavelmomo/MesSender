import { Text } from "react-native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const loginMock = () => {
  return <Text>Login page</Text>;
};
const dialogsMock = () => {
  return <Text>Молодец Авторизовался!</Text>;
};

export const AuthRoutes = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Login" component={loginMock} />
      <Stack.Screen name="Register" component={loginMock} />
    </Stack.Navigator>
  );
};

export const AppRoutes = () => {
  return (
    <Tab.Navigator>
      <Stack.Screen name="Dialogs" component={dialogsMock} />
      <Stack.Screen name="Users" component={dialogsMock} />
      <Stack.Screen name="Profiles" component={dialogsMock} />
    </Tab.Navigator>
  );
};
