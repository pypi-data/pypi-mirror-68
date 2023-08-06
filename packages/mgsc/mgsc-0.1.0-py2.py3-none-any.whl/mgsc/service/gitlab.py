from mgsc.service.service import GitService
from mgsc.blueprints import Repository, Namespace


class Gitlab(GitService):
    @property
    def servertype(self):
        return "gitlab"

    @property
    def repositories(self) -> Repository:
        all_repos = self.session.httpaction(
            http_verb="get", path=f"/users/{self.userid}/projects?per_page=2000"
        ).json()

        for repo in all_repos:
            yield Repository(
                name=repo["name"],
                namespace=Namespace(repo["namespace"]["path"]),
                ssh_url=repo["ssh_url_to_repo"],
                http_url=repo["http_url_to_repo"],
                localfs_url=None,
                description=repo["description"],
            )

    def get_namespace_repos(self, namespace):
        namespace_dict = self.session.httpaction(
            "get", f"/namespaces/{namespace.name}"
        ).json()

        if namespace_dict["kind"] == "user":
            for repo in self.repositories:
                yield repo
        else:
            group_projects = self.session.httpaction(
                "get", f"/groups/{namespace}"
            ).json()["projects"]

            for repo in group_projects:
                yield Repository(
                    name=repo["name"],
                    namespace=namespace,
                    ssh_url=repo["ssh_url_to_repo"],
                    http_url=repo["http_url_to_repo"],
                    localfs_url=None,
                    description=repo["description"],
                )

    def get_namespaces(self, namespace=None) -> Namespace:
        namespaces = self.session.httpaction(
            http_verb="get", path=f'/namespaces/{namespace or ""}'
        ).json()

        for ns in namespaces:
            yield Namespace(
                name=Namespace(ns["path"]),
                parent=namespace,
                repositories=self.get_namespace_repos(Namespace(ns["path"])),
            )

    @property
    def userid(self):
        userid = self.session.httpaction("get", "/user").json()["id"]

        return userid

    def create_namespace(self):
        raise NotImplementedError()

    def create_repository(self):
        raise NotImplementedError()
