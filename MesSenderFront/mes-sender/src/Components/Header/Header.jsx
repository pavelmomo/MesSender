import './Header.css'

function Header ()
{
    return (
        <>
          <header className='menu'>
            <nav>
              <ul>
                <a href=''>Профиль</a>
                <a href=''>Диалоги</a>
                <a href=''>Пользователи</a>
              </ul>
            </nav>
          </header>
        </>
      );
};

export default Header;