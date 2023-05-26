import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import { HomeData } from "./components/pages/Home";
import {
  BookOut,
  BookIn,
  Author,
  AuthorDetails,
  Genre,
  Tokens,
  Language,
  ErrorObject,
  CopyIn,
  SignupData,
  Genre as GenreDetails,
  LanguageDetails,
  UserDetails,
  CopyOut,
  Status,
  BorrowedIn,
  BorrowedOut,
} from "./CustomTypes";
import jwt_decode from "jwt-decode";
import { DecodedRefreshToken } from "./contexts/AuthContext";

export class APIClient {
  /**
   * This class handles all the calls to the Django Rest Api
   * The class is a singleton, and uses an Axios Instance as an attribute
   */

  private static axiosInstance: AxiosInstance;
  private static instance: APIClient;

  //The constructor creates an axiosInstance
  private constructor(options: AxiosRequestConfig) {
    APIClient.axiosInstance = axios.create(options);
  }

  //The getInstance method returns an instance of the class to be used
  public static getInstance(options: AxiosRequestConfig): APIClient {
    if (!APIClient.instance) {
      APIClient.instance = new APIClient(options);
      APIClient.instance.getInterceptors();
    }
    return APIClient.instance;
  }

  private handleErrors(error: any): ErrorObject | undefined {
    console.log(error);
    if (error.response) {
      const err: ErrorObject = {
        status: error.response.status,
        message: error.response.data.detail,
      };
      return err;
    }
  }

  //This method uses api call to get book details using id. It returns the received details.
  public GetBookDetails(id: string): Promise<BookIn> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/book/" + id)
        .then((res) => {
          const book: BookIn = this.bookDeserialize(res.data.data);
          resolve(book);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method uses book post api to create a new book
  public CreateBook(book: BookOut): Promise<number> {
    return APIClient.axiosInstance
      .post("/book/", this.bookSerialize(book))
      .then((res) => {
        // An id is assigned to book once its saved in backend server
        const id: number = res.data.data.id;
        return id;
      });
  }

  // This method uses book put api to edit a book
  public UpdateBook(book: BookOut, id: number): Promise<boolean> {
    return APIClient.axiosInstance
      .put("/book/" + String(id) + "/", this.bookSerialize(book))
      .then((res) => {
        return true;
      });
  }

  // This method deletes book using delete api for book
  public DeleteBook(id: string): Promise<boolean> {
    return APIClient.axiosInstance.delete("/book/" + id + "/").then((res) => {
      return true;
    });
  }

  // This method converts a Book object from json to Book interface
  private bookDeserialize(json: any): BookIn {
    let book: BookIn = json;

    book.authors = json.authors;
    book.language = json.language;
    book.genres = json.genres;
    book.dateOfPublication = json.date_of_publication.substring(0, 10);
    return book;
  }

  // This method converts a Book object from json to Book interface
  public bookSerialize(book: BookOut) {
    let serialized = {
      title: book.title,
      author_ids: book.authorIds,
      description: book.description,
      isbn: book.isbn,
      language_id: book.languageId,
      genre_ids: book.genreIds,
      date_of_publication: book.dateOfPublication,
      no_of_copies: book.numberOfCopies,
    };

    return serialized;
  }

  //This method uses api call to fetch list of books. It returns this list.
  public GetBookList(pagenumber: number): Promise<BookIn[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`book/?page_number=${pagenumber}&page_size=10`)
        .then((response) => {
          let bookList: BookIn[] = [];

          for (let data of response.data.data) {
            bookList.push(this.bookDeserialize(data));
          }

          resolve(bookList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public genreSerialize(genre: Genre): any {
    return {
      genre: genre.genre,
    };
  }

  public GetBooksForAuthor(authorId: string): Promise<BookIn[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`/book/?author=${authorId}`)
        .then((response) => {
          let bookList: BookIn[] = [];

          for (let data of response.data.data) {
            bookList.push(this.bookDeserialize(data));
          }

          resolve(bookList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public GetBooksForGenre(genreId: string): Promise<BookIn[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`/book/?genre=${genreId}`)
        .then((response) => {
          let bookList: BookIn[] = [];

          for (let data of response.data.data) {
            bookList.push(this.bookDeserialize(data));
          }

          resolve(bookList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public GetBooksForLanguages(languageid: string): Promise<BookIn[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`/book/?language=${languageid}`)
        .then((response) => {
          let bookList: BookIn[] = [];

          for (let data of response.data.data) {
            bookList.push(this.bookDeserialize(data));
          }

          resolve(bookList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  private copyDeserialize(json: any): CopyIn {
    let copy: CopyIn = json;

    copy.id = json.id;
    copy.book = this.bookDeserialize(json.book);
    copy.language = json.language;
    copy.status = json.status;
    return copy;
  }

  // This method converts a Book object from json to Book interface
  public copySerializer(copy: CopyOut) {
    let serialized = {
      book_id: copy.bookId,
      language_id: copy.languageId,
      status_id: copy.statusId,
    };

    return serialized;
  }

  public GetCopiesofBook(bookId: string): Promise<CopyIn[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`/copy/book/${bookId}`)
        .then((res) => {
          const copies: CopyIn[] = res.data.data.map((copy: any) =>
            this.copyDeserialize(copy)
          );
          resolve(copies);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public CreateCopy(copy: CopyOut): Promise<number> {
    return APIClient.axiosInstance
      .post("/copy/", this.copySerializer(copy))
      .then((res) => {
        // An id is assigned to copy once its saved in backend server
        const id: number = res.data.data.id;
        return id;
      });
  }

  public GetCopyDetails(id: string): Promise<CopyIn> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/copy/" + id)
        .then((res) => {
          const copy: CopyIn = this.copyDeserialize(res.data.data);
          resolve(copy);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public UpdateCopy(copy: CopyOut, id: number): Promise<boolean> {
    return APIClient.axiosInstance
      .put("/copy/" + String(id) + "/", this.copySerializer(copy))
      .then((res) => {
        return true;
      });
  }

  public DeleteCopy(id: string): Promise<boolean> {
    return APIClient.axiosInstance.delete("/copy/" + id + "/").then((res) => {
      return true;
    });
  }

  // This method fetches and returns the genre using its id.
  public GetGenreDetails(id: number): Promise<Genre> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`/genre/${id}`)
        .then((res) => {
          const genre: Genre = res.data.data;
          resolve(genre);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method fetches and returns the all genres.
  public GetAllGenres(): Promise<Genre[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/genre")
        .then((res) => {
          const genreList: Genre[] = res.data.data;
          resolve(genreList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }
  public PostGenre(GenreData: GenreDetails): Promise<number> {
    return APIClient.axiosInstance.post("/genre/", GenreData).then((res) => {
      // Redirect to the details page of the currently created genre
      const id: number = res.data.data.id;
      return id;
    });
  }
  public PutGenre(genre: Genre, id: number): Promise<boolean> {
    return APIClient.axiosInstance
      .put(`/genre/${id}`, this.genreSerialize(genre))
      .then((res) => {
        return true;
      });
  }
  // This method deletes book using delete api for book
  public DeleteGenre(id: string): Promise<boolean> {
    return APIClient.axiosInstance.delete("/genre/" + id + "/").then((res) => {
      return true;
    });
  }

  public GetAllStatuses(): Promise<Status[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/status/")
        .then((res) => {
          const statuses: Status[] = res.data.data;
          resolve(statuses);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method fetches and returns all languages
  public GetAllLanguages(): Promise<Language[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/language")
        .then((res) => {
          const languageList: Language[] = res.data.data;
          resolve(languageList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public DeleteLanguage(id: string): Promise<boolean> {
    return APIClient.axiosInstance.delete("/language/" + id).then((res) => {
      return true;
    });
  }

  public PutLanguage(id: string, data: Language): Promise<Boolean> {
    return APIClient.axiosInstance.put("/language/" + id, data).then((res) => {
      return true;
    });
  }

  // public PutAuthor(id: string, data: AuthorDetails): Promise<Boolean> {
  //   return APIClient.axiosInstance
  //     .put("/author/" + id + "/", data)
  //     .then((res) => {
  //       return true;
  //     });
  // }

  // This method fetches and returns the language using its id.
  public GetLanguageDetails(id: string): Promise<Language> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`/language/${id}`)
        .then((res) => {
          const language: Language = res.data.data;
          resolve(language);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  //Used to get the detauls of an author
  public GetAuthorDetails(id: string): Promise<Author> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/author/" + id)
        .then((res) => {
          const author: Author = res.data.data;
          resolve(author);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  //Used to get data needed to fill the home page
  public GetHomePageData(): Promise<HomeData> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/home")
        .then((res) => {
          let HomePageData: HomeData = res.data.data;
          resolve(HomePageData);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  //Used to get a list of all the authors
  public GetAuthorsList(page: number): Promise<Author[]> {
    return new Promise((resolve, reject) => {
      let authorList: Author[];
      APIClient.axiosInstance
        .get(`/author?page_number=${page}&page_size=10`)
        .then((response) => {
          authorList = response.data.data;
          resolve(authorList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public GetUsersList(): Promise<UserDetails[]> {
    return new Promise((resolve, reject) => {
      let userList: UserDetails[];
      APIClient.axiosInstance
        .get("/user")
        .then((response) => {
          userList = response.data.data;
          resolve(userList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public GetUserDetails(id: string): Promise<UserDetails> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/user/" + id)
        .then((res) => {
          const user: UserDetails = res.data.data;
          resolve(user);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public async PutUser(id: string, data: UserDetails): Promise<Boolean> {
    const res = await APIClient.axiosInstance.put("/user/" + id + "/", data);
    return true;
  }

  public async UpdateMe(data: UserDetails): Promise<Boolean> {
    const res = await APIClient.axiosInstance.put("/user/", data);
    return true;
  }

  //Used to get access and refresh tokens for the login component
  public Login(data: FormData): Promise<Tokens> {
    return APIClient.axiosInstance.post("/auth/token", data).then((res) => {
      let tokens: Tokens = {
        access_token: res.data.data.access_token,
        refresh_token: res.data.data.refresh_token,
      };
      let user: UserDetails = res.data.data;
      localStorage.setItem("access_token", tokens.access_token);
      localStorage.setItem("refresh_token", tokens.refresh_token);
      localStorage.setItem("user", JSON.stringify(user));
      APIClient.instance.SetAuthorizationHeaders(
        "Bearer " + tokens.access_token
      );
      return tokens;
    });
  }

  public Signup(data: SignupData): Promise<Tokens> {
    return APIClient.axiosInstance.post("/auth/register", data).then((res) => {
      let tokens: Tokens = {
        access_token: res.data.data.access_token,
        refresh_token: res.data.data.refresh_token,
      };
      localStorage.setItem("access_token", tokens.access_token);
      localStorage.setItem("refresh_token", tokens.refresh_token);
      APIClient.instance.SetAuthorizationHeaders(
        "Bearer " + tokens.access_token
      );
      return tokens;
    });
  }

  public LibrarianSignup(data: SignupData): Promise<Boolean> {
    return APIClient.axiosInstance
      .post("/auth/librarian/register", data)
      .then((res) => {
        return true;
      });
  }

  //Used to set the authorization headers with the access token for the axios instant
  private SetAuthorizationHeaders(TokenHeader: String | null): void {
    APIClient.axiosInstance.defaults.headers["Authorization"] = TokenHeader;
  }

  //Used to clear the access and refresh tokens, remove them from the authorization headers and add the refresh token to
  //the blacklist app
  public Logout(): Promise<boolean> {
    return APIClient.axiosInstance
      .post("/auth/logout", {
        refresh_token: localStorage.getItem("refresh_token"),
      })
      .then((res) => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        APIClient.instance.SetAuthorizationHeaders(null);
        return true;
      });
  }

  //Used to create a new author from the create author component
  public PostAuthor(AuthorData: AuthorDetails): Promise<Number> {
    return APIClient.axiosInstance.post("/author/", AuthorData).then((res) => {
      //Redirect to the details page of the currently created author
      const id: Number = res.data.data.id;
      return id;
    });
  }

  //Used to delete a given author from the delete author page
  public DeleteAuthor(id: string): Promise<Boolean> {
    return APIClient.axiosInstance.delete("/author/" + id + "/").then((res) => {
      return true;
    });
  }
  public DeleteUser(id: string): Promise<Boolean> {
    return APIClient.axiosInstance.delete("/user/" + id + "/").then((res) => {
      return true;
    });
  }

  //Used to update a given authors data
  public PutAuthor(id: string, data: AuthorDetails): Promise<Boolean> {
    return APIClient.axiosInstance
      .put("/author/" + id + "/", data)
      .then((res) => {
        return true;
      });
  }

  public PostLanguage(Language: Language): Promise<Number> {
    return APIClient.axiosInstance.post("/language/", Language).then((res) => {
      //Redirect to the details page of the currently created language
      const id: Number = res.data.data.language_id;
      console.log(id);
      return id;
    });
  }

  private borrowedDeserialize(json: any): BorrowedIn {
    let borrowed: BorrowedIn = json;

    borrowed.id = json.id;
    borrowed.copy = this.copyDeserialize(json.copy);
    borrowed.user = json.user;
    borrowed.dueDate = json.due_date;
    borrowed.issueDate = json.issue_date;
    borrowed.returnDate = json.return_date;
    return borrowed;
  }

  public borrowedSerialize(borrowed: BorrowedOut) {
    let serialized = {
      copy_id: borrowed.copyId,
      user_id: borrowed.userId,
      due_date: borrowed.dueDate,
      issue_date: borrowed.issueDate,
      return_date: borrowed.returnDate,
    };

    return serialized;
  }

  public GetMyBorrowed(): Promise<BorrowedIn[]> {
    return new Promise((resolve, reject) => {
      let myBorrowed: BorrowedIn[];
      APIClient.axiosInstance
        .get("/borrowed/user")
        .then((response) => {
          myBorrowed = response.data.data.map((borrowed: any) =>
            this.borrowedDeserialize(borrowed)
          );
          resolve(myBorrowed);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public GetBorrowedForUser(id: string): Promise<BorrowedIn[]> {
    return new Promise((resolve, reject) => {
      let myBorrowed: BorrowedIn[];
      APIClient.axiosInstance
        .get("/borrowed/user/" + id)
        .then((response) => {
          myBorrowed = response.data.data.map((borrowed: any) =>
            this.borrowedDeserialize(borrowed)
          );
          resolve(myBorrowed);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public CreateBorrowed(borrowed: BorrowedOut): Promise<number> {
    return APIClient.axiosInstance
      .post("/borrowed/", this.borrowedSerialize(borrowed))
      .then((res) => {
        // An id is assigned to book once its saved in backend server
        const id: number = res.data.data.id;
        return id;
      });
  }

  public GetBorrowedDetails(id: string): Promise<BorrowedIn> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`/borrowed/${id}`)
        .then((res) => {
          const borrowed: BorrowedIn = this.borrowedDeserialize(res.data.data);
          resolve(borrowed);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  public ReturnBorrowed(id: string, data: BorrowedOut): Promise<Boolean> {
    return APIClient.axiosInstance
      .put("/borrowed/return_borrowed_user/" + id, data)
      .then((res) => {
        return true;
      });
  }

  public UpdateBorrowed(id: string, data: BorrowedOut): Promise<Boolean> {
    return APIClient.axiosInstance.put("/borrowed/" + id, data).then((res) => {
      return true;
    });
  }

  public DeleteBorrowed(id: string): Promise<Boolean> {
    return APIClient.axiosInstance
      .delete("/borrowed/" + id + "/")
      .then((res) => {
        return true;
      });
  }

  //Helper function for the axios interceptors.
  //Used to get a new access token using a refresh token
  private UseRefreshToken(refreshToken: string): Promise<string> {
    return APIClient.axiosInstance
      .post("/auth/refresh_token", { refresh_token: refreshToken })
      .then((response) => {
        const access_token: string = response.data.data.access_token;
        localStorage.setItem("access_token", access_token);
        APIClient.instance.SetAuthorizationHeaders("Bearer " + access_token);
        return access_token;
      });
  }
  //Used to intercept certain responses
  private getInterceptors() {
    APIClient.axiosInstance.interceptors.response.use(
      (response) => {
        //If the status code for the response is 2XX, do nothing and send the response forward
        return response;
      },
      (error) => {
        //If the status code is not 2XX
        //Process the request.
        const originalrequest = error.config;
        if (error.response) {
          if (error.response.status === 401 && !originalrequest._retry) {
            //If the status code is 401 and the request has not been retried before,
            //Check to see if the refresh token is valid
            originalrequest._retry = true;
            const refreshToken = localStorage.getItem("refresh_token");
            if (refreshToken != null) {
              const decoded_token: DecodedRefreshToken =
                jwt_decode(refreshToken);
              if (decoded_token.exp < Math.ceil(Date.now() / 1000)) {
                //if the refresh token is expired, logout the user and remove the access and refresh tokens,
                //redirect the user to the login page
                localStorage.removeItem("refresh_token");
                localStorage.removeItem("access_token");
                window.location.href = "/login/";
              }
              return APIClient.instance
                .UseRefreshToken(refreshToken)
                .then((access_token) => {
                  //If the refresh token is valid, generate a new access token and retry the original request
                  //with the new access token in the authorization header
                  originalrequest.headers["Authorization"] =
                    "Bearer " + access_token;
                  return APIClient.axiosInstance(originalrequest);
                });
            }
            //If the refresh token is not available, logout the user and redirect them to the login page
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("access_token");
            window.location.href = "/login/";
          }
          return Promise.reject(error);
        }
        return Promise.reject(error);
      }
    );
  }
}

export const client = APIClient.getInstance({
  /**
   * This is the axios instance used by the entire frontend app.
   * When a user logs in, the Authorization details are stored here so that all future requests use them.
   * Axios interceptors will also be added to help with refreshing the access token and error handling in the future
   */
  timeout: 5000,
  headers: {
    Authorization: localStorage.getItem("access_token")
      ? "Bearer " + localStorage.getItem("access_token")
      : null,
    "Content-Type": "application/json",
    accept: "application/json",
  },
  baseURL: "http://16.171.21.166:8000/",
  // transformResponse: [(response) =>{
  //   console.log(response.data.data)
  // 	return response.data.data
  // }]
});
