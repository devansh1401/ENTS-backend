import { React } from 'react';
import AddCellModal from './components/AddCellModal';
import useAuth from '../../auth/hooks/useAuth';
import Nav from '../../components/Nav';

function Profile() {
  const { user, loggedIn } = useAuth();
  return (
    <>
      <Nav />
      {loggedIn === true ? (
        <>
          <p>Logged in as {user.first_name}</p> <AddCellModal />
        </>
      ) : (
        <h1>NOT LOGGED IN!</h1>
      )}
    </>
  );
}

export default Profile;
