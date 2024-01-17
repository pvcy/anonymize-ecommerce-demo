# Anonymize ecommerce API demo

This is a demonstration repository that uses a Neon serverless database and an ArgoCD server to build and test a preview environment for each pull request.

To use this you will need:

- A fork of this repo
- A subdomain with a wildcard DNS
- An ArgoCD server with a public ingress (so GitHub Actions can access it)
  - Create an ApplicationSet in your Argo CD instance using the example included here (`application-set.yaml`)
  - Use an ingress controller and wildcard certificates so that `*.your-domain.com` resolves to your Argo CD based previews
- A [Neon](https://neon.tech/) account (a free trial is available)
  - **Note:** The app itself can use any accessible PostgreSQL database, but the preview demo currently depends on [Neon's Branching feature](https://neon.tech/branching).
- GitHub Secrets for the workflow:
  - NEON_API_KEY - An api key for your Neon account
  - NEON_PROJECT_ID - The project ID in Neon
  - ARGOCD_HOSTNAME - The public ingress for your Argo CD installation
  - ARGOCD_USERNAME - The Argo CD username
  - ARGOCD_PASSWORD - The Argo CD password
  - GHCR_EMAIL - The email address used to create packages in the GitHub Container Registry
  - GHCR_TOKEN - A personal access token with [permission to create packages](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
  - PREVIEW_DOMAIN - A subdomain where the previews will be hosted. e.g. `your-domain.com` will result in previews at `https://preview-pr-123.your-domain.com`

You will need to restore the database backup from the `example_data` folder into your database host.

To test locally set a variable with connection string and use Docker Compose:

```
$ export DB_CONNSTRING="postgresql://USERNAME:PASSWORD@DB-HOST/DB_NAME"

$ docker-compose up
```

## Acknowledgement:

The design of the preview environment was inspired significantly by Neon's [kube-previews-manifests](https://github.com/neondatabase/kube-previews-manifests/tree/main) and the [accompanying blog post](https://neon.tech/blog/preview-environments-neon-kubernetes-argo-cd).
