import weaviate
import weaviate.classes as wvc

client = weaviate.connect_to_local()


def delete_uuid_from_json(uuid):
    authors = client.collections.get("Question")
    # authors = authors.with_tenant("tenantA")  # Optional; specify the tenant in multi-tenancy collections
    # authors = authors.with_consistency_level(wvc.config.ConsistencyLevel.QUORUM)  # Optional; specify the consistency level
    for elem in authors.find():
        input(elem)
    response = authors.data.delete_many(
        where=wvc.query.Filter.by_property("id").equal(uuid),
        verbose=True,
        dry_run=False,
    )

    print(f"Matched {response.matches} objects.")
    print(f"Deleted {response.successful} objects.")
