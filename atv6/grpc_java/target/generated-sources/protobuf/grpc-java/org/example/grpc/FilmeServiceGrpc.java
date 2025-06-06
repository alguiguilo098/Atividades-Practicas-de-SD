package org.example.grpc;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.63.0)",
    comments = "Source: mflix.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class FilmeServiceGrpc {

  private FilmeServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "org.example.grpc.FilmeService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<org.example.grpc.FilmePedido,
      org.example.grpc.PedidoResposta> getGerenciaFilmesMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GerenciaFilmes",
      requestType = org.example.grpc.FilmePedido.class,
      responseType = org.example.grpc.PedidoResposta.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<org.example.grpc.FilmePedido,
      org.example.grpc.PedidoResposta> getGerenciaFilmesMethod() {
    io.grpc.MethodDescriptor<org.example.grpc.FilmePedido, org.example.grpc.PedidoResposta> getGerenciaFilmesMethod;
    if ((getGerenciaFilmesMethod = FilmeServiceGrpc.getGerenciaFilmesMethod) == null) {
      synchronized (FilmeServiceGrpc.class) {
        if ((getGerenciaFilmesMethod = FilmeServiceGrpc.getGerenciaFilmesMethod) == null) {
          FilmeServiceGrpc.getGerenciaFilmesMethod = getGerenciaFilmesMethod =
              io.grpc.MethodDescriptor.<org.example.grpc.FilmePedido, org.example.grpc.PedidoResposta>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GerenciaFilmes"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  org.example.grpc.FilmePedido.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  org.example.grpc.PedidoResposta.getDefaultInstance()))
              .setSchemaDescriptor(new FilmeServiceMethodDescriptorSupplier("GerenciaFilmes"))
              .build();
        }
      }
    }
    return getGerenciaFilmesMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static FilmeServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<FilmeServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<FilmeServiceStub>() {
        @java.lang.Override
        public FilmeServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new FilmeServiceStub(channel, callOptions);
        }
      };
    return FilmeServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static FilmeServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<FilmeServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<FilmeServiceBlockingStub>() {
        @java.lang.Override
        public FilmeServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new FilmeServiceBlockingStub(channel, callOptions);
        }
      };
    return FilmeServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static FilmeServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<FilmeServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<FilmeServiceFutureStub>() {
        @java.lang.Override
        public FilmeServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new FilmeServiceFutureStub(channel, callOptions);
        }
      };
    return FilmeServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void gerenciaFilmes(org.example.grpc.FilmePedido request,
        io.grpc.stub.StreamObserver<org.example.grpc.PedidoResposta> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGerenciaFilmesMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service FilmeService.
   */
  public static abstract class FilmeServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return FilmeServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service FilmeService.
   */
  public static final class FilmeServiceStub
      extends io.grpc.stub.AbstractAsyncStub<FilmeServiceStub> {
    private FilmeServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected FilmeServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new FilmeServiceStub(channel, callOptions);
    }

    /**
     */
    public void gerenciaFilmes(org.example.grpc.FilmePedido request,
        io.grpc.stub.StreamObserver<org.example.grpc.PedidoResposta> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGerenciaFilmesMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service FilmeService.
   */
  public static final class FilmeServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<FilmeServiceBlockingStub> {
    private FilmeServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected FilmeServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new FilmeServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public org.example.grpc.PedidoResposta gerenciaFilmes(org.example.grpc.FilmePedido request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGerenciaFilmesMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service FilmeService.
   */
  public static final class FilmeServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<FilmeServiceFutureStub> {
    private FilmeServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected FilmeServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new FilmeServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<org.example.grpc.PedidoResposta> gerenciaFilmes(
        org.example.grpc.FilmePedido request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGerenciaFilmesMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_GERENCIA_FILMES = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_GERENCIA_FILMES:
          serviceImpl.gerenciaFilmes((org.example.grpc.FilmePedido) request,
              (io.grpc.stub.StreamObserver<org.example.grpc.PedidoResposta>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getGerenciaFilmesMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              org.example.grpc.FilmePedido,
              org.example.grpc.PedidoResposta>(
                service, METHODID_GERENCIA_FILMES)))
        .build();
  }

  private static abstract class FilmeServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    FilmeServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return org.example.grpc.Mflix.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("FilmeService");
    }
  }

  private static final class FilmeServiceFileDescriptorSupplier
      extends FilmeServiceBaseDescriptorSupplier {
    FilmeServiceFileDescriptorSupplier() {}
  }

  private static final class FilmeServiceMethodDescriptorSupplier
      extends FilmeServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    FilmeServiceMethodDescriptorSupplier(java.lang.String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (FilmeServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new FilmeServiceFileDescriptorSupplier())
              .addMethod(getGerenciaFilmesMethod())
              .build();
        }
      }
    }
    return result;
  }
}
