import React, { ReactElement, useEffect, useState, useContext } from 'react';
import { client } from '../../axios';
import { useParams, useHistory } from 'react-router-dom';
import UserForm from './UserForm';
import { SubmitHandler } from 'react-hook-form';
import { ErrorObject, UserDetails } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import { AuthContext } from '../../contexts/AuthContext';

interface Props {}

function UserUpdate(props: Props): ReactElement {
  const { id }: { id: string } = useParams();
  const userId: number = parseInt(id); // Parse id as a number
  const history = useHistory();

  const [user, setUser] = useState<UserDetails | null>(null);
  const [loaded, setLoaded] = useState<boolean>(false);
  const [error, setError] = useState<ErrorObject>();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } = useContext(AuthContext);

  useEffect(() => {
    client
      .GetUserDetails(id)
      .then((userData) => {
        if (userData) {
          setUser(userData);
          setLoaded(true);
        }
      })
      .catch((error) => {
        setError(error);
      });
  }, [userId]);

  useEffect(() => {
    if (isAuthenticated === true) {
      if (isLibrarian !== true) {
        let err: ErrorObject = {
          status: 403,
          message: 'Forbidden. You do not have permission to view this page',
        };
        setError(err);
      }
    } else {
      let err: ErrorObject = {
        status: 401,
        message: 'Unauthorized, you must be logged in to view this page',
      };
      setError(err);
    }
  }, [isAuthenticated, isLibrarian]);

  const onSubmit: SubmitHandler<UserDetails> = (data) => {
    client
      .PutUser(id,data)
      .then((response) => {
        history.push('/user/' + userId);
      });
  };

  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div className='background-image'>
      {loaded === true ? (
        <UserForm user={user} onSubmit={onSubmit} />
      ) : (
        <h1>--Loading--</h1>
      )}
    </div>
  );
}

export default UserUpdate;
