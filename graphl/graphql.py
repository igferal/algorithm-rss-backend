from app import app, db
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from models import PostModel, UserModel

class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (graphene.relay.Node,)


class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        username = graphene.String(required=True)

    post = graphene.Field(lambda: PostObject)

    def mutate(self, info, title, body, username):
        user = UserModel.query.filter_by(username=username).first()
        post = PostModel(title=title, body=body)
        if user is not None:
            post.author = user
        db.session.add(post)
        db.session.commit()
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)