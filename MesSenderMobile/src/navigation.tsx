import { Text } from "react-native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const LoginMock = () => {
  return <Text>Login page</Text>;
};
const DialogsMock = () => {
  return <Text>Молодец Авторизовался!</Text>;
};

export const AuthRoutes = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Login" component={LoginMock} />
      <Stack.Screen name="Register" component={LoginMock} />
    </Stack.Navigator>
  );
};

export const AppRoutes = () => {
  return (
    <Tab.Navigator>
      <Stack.Screen name="Dialogs" component={DialogsMock} />
      <Stack.Screen name="Users" component={DialogsMock} />
      <Stack.Screen name="Profiles" component={DialogsMock} />
    </Tab.Navigator>
  );
};
