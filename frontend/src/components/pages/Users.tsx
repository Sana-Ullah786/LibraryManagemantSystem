import React, { useEffect, useState, useContext } from 'react';
import { client } from '../../axios';
import UserListItem from './UserListItem';
import { Link, useRouteMatch } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';
import { UserDetails, ErrorObject } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import '../style.css'; // Import the Users CSS file
import ScrollView from '../Scrollview';
function Users() {
    const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

    let { url }: { url: string } = useRouteMatch();

    const [userList, setUserList] = useState<UserDetails[]>([]);
    const [error, setError] = useState<ErrorObject>();

    useEffect(() => {
        client
            .GetUsersList()
            .then((userList) => {
                if (userList) {
                    setUserList(userList);
                }
            })
            .catch((error) => {
                setError(error);
            });
    }, []);

    function setUserListItemComponent(userList: UserDetails[]) {
        const userListItemComponent: JSX.Element[] = userList.map((user) => {
            if (!user.id) {
                return (
                    <li key={null}>
                        No items
                    </li>
                );
            } else {
                return (
                    <li className="user-list-item" key={user.id.toString()}>
                        <UserListItem
                            key={user.id}
                            item={user}
                            linksto={`${url}/${user.id}`}
                        />
                    </li>
                );
            }
        });
        return userListItemComponent;
    }

    function createUserLink() {
        return (
            <Link to={`/users/create`} className="genre-link">
                Create User
            </Link>
        );
    }

    if (error != null) {
        return <ErrorComponent error={error} />;
    }

    return (
        <div className="user-list background-image">
            <div className='modal'>
                <h1>User List</h1>
                <ScrollView>
                    <ul>
                        {setUserListItemComponent(userList)}
                    </ul>
                </ScrollView>
                {isLibrarian ? createUserLink() : null}
            </div>
        </div>
    );
}

export default Users;
