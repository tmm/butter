import React from "react";
import { observer, Provider } from "mobx-react";
import { BrowserRouter, Switch, Route, Redirect } from "react-router-dom";
import DocumentTitle from "react-document-title";
import RootStore from "./store";
import { get } from "./lib/get";
import { ThemeProvider, Navbar, PrivateRoute, PublicRoute } from "./components";
import {
    NoMatch,
    Budgets,
    Register,
    LogIn,
    Budget,
    Accounts,
    Transaction,
    Transactions
} from "./pages";

class App extends React.Component {
    rootStore = new RootStore();

    componentWillMount() {
        const user = get(() =>
            JSON.parse(localStorage.getItem("user") as string)
        );
        if (user) {
            this.rootStore.setUser(user);
        }
    }

    render() {
        const { isAuthenticated, userInitial, logOut } = this.rootStore;
        return (
            <ThemeProvider>
                <Provider rootStore={this.rootStore}>
                    <DocumentTitle title="Wilbur">
                        <BrowserRouter>
                            <React.Fragment>
                                {isAuthenticated && (
                                    <Navbar
                                        location={location}
                                        userInitial={userInitial}
                                        handleLogOut={logOut}
                                    />
                                )}
                                <Switch>
                                    <Route path="/login" component={LogIn} />
                                    <PublicRoute
                                        path="/register"
                                        component={Register}
                                        isAuthenticated={isAuthenticated}
                                    />
                                    <PrivateRoute
                                        path="/accounts"
                                        component={Accounts}
                                        isAuthenticated={isAuthenticated}
                                    />
                                    <PrivateRoute
                                        path="/budgets/:id"
                                        component={Budget}
                                        isAuthenticated={isAuthenticated}
                                    />
                                    <PrivateRoute
                                        path="/budgets"
                                        component={Budgets}
                                        isAuthenticated={isAuthenticated}
                                    />
                                    <PrivateRoute
                                        path="/transactions/:id"
                                        component={Transaction}
                                        isAuthenticated={isAuthenticated}
                                    />
                                    <PrivateRoute
                                        path="/transactions"
                                        component={Transactions}
                                        isAuthenticated={isAuthenticated}
                                    />
                                    <Route
                                        path="/"
                                        render={() => (
                                            <Redirect to="/budgets" />
                                        )}
                                    />
                                    <Route component={NoMatch} />
                                </Switch>
                            </React.Fragment>
                        </BrowserRouter>
                    </DocumentTitle>
                </Provider>
            </ThemeProvider>
        );
    }
}

export default observer(App);