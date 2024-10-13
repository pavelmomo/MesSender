import { BASE_HTTP_URL } from "../constant/app";

export async function getCurrentUser(token: string): Promise<UserDTO | null> {
  try {
    const response = await fetch(BASE_HTTP_URL + `api/users/me`, {
      headers: { Authorization: token },
    });
    switch (response.status) {
      case 200:
        return await response.json();
        break;
      default:
        throw Error(
          "Ошибка при обращении к серверу. Статус ответа: " + response.status
        );
    }
  } catch (err) {
    console.log(err);
    return null;
  }
}
